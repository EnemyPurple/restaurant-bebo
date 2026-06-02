from __future__ import annotations

import json
import shutil
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.booking.models import Table
from apps.core.bundled import db_snapshot_path, restore_db_snapshot
from apps.events.models import Event
from apps.gallery.models import GalleryImage
from apps.menu.models import Category, Dish


class Command(BaseCommand):
    help = "Copy bundled assets and restore full DB snapshot on deploy (Render)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--seed-db",
            action="store_true",
            help="Force full DB restore from assets/bundled/db.json (ignores preserve mode)",
        )

    def handle(self, *args, **options):
        bundled_root = settings.BASE_DIR / "assets" / "bundled"
        manifest_path = bundled_root / "manifest.json"
        if not bundled_root.exists():
            self.stdout.write(self.style.WARNING("No assets/bundled folder found, skipping."))
            return

        mode = getattr(settings, "BUNDLED_MEDIA_MODE", "full")
        if options.get("seed_db"):
            mode = "full"
        if mode == "off":
            self.stdout.write(self.style.WARNING("Bundled media sync disabled (BUNDLED_MEDIA_MODE=off)."))
            return

        copied = self._copy_tree(bundled_root / "static", settings.BASE_DIR / "static", overwrite=True)
        copied += self._copy_tree(bundled_root / "media", settings.MEDIA_ROOT, overwrite=True)
        self.stdout.write(f"Synced {copied} bundled file(s) to static/media.")

        if mode in ("media-only", "preserve"):
            cache.delete("menu:categories")
            if mode == "preserve":
                self.stdout.write(
                    self.style.WARNING(
                        "Preserve mode: database left unchanged. "
                        "Use sync_bundled_media --seed-db to restore from db.json."
                    )
                )
            self.stdout.write(self.style.SUCCESS("Bundled media sync completed."))
            return

        snapshot = db_snapshot_path()
        if snapshot.is_file():
            loaded = restore_db_snapshot()
            cache.delete("menu:categories")
            self.stdout.write(self.style.SUCCESS(f"Restored full DB snapshot ({loaded} object(s))."))
            self.stdout.write(self.style.SUCCESS("Bundled media sync completed."))
            return

        if not manifest_path.exists():
            self.stdout.write(self.style.WARNING("No db.json or manifest.json found, skipping DB seed."))
            return

        self.stdout.write(self.style.WARNING("db.json missing — falling back to manifest.json seed."))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self._seed_categories(manifest.get("categories", []))
        self._deactivate_dishes(manifest.get("deactivate_dishes", []))
        dishes = manifest.get("dishes", [])
        self._seed_dishes(dishes)
        self._prune_dishes(dishes)
        self._prune_categories(manifest.get("categories", []))
        self._seed_gallery(manifest.get("gallery", []))
        self._seed_events(manifest.get("events", []))
        self._seed_tables(manifest.get("tables", []))
        self._prune_tables(manifest.get("tables", []))
        cache.delete("menu:categories")
        self.stdout.write(self.style.SUCCESS("Bundled media sync completed."))

    def _copy_tree(self, src: Path, dst: Path, *, overwrite: bool) -> int:
        if not src.exists():
            return 0
        copied = 0
        for file_path in src.rglob("*"):
            if not file_path.is_file():
                continue
            rel = file_path.relative_to(src)
            target = dst / rel
            if target.exists() and not overwrite:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, target)
            copied += 1
        return copied

    def _seed_categories(self, items: list[dict]) -> None:
        for item in items:
            category, _ = Category.objects.get_or_create(
                name=item["name"],
                defaults={"sort_order": item.get("sort_order", 0), "is_active": True},
            )
            sort_order = item.get("sort_order", 0)
            if category.sort_order != sort_order or not category.is_active:
                category.sort_order = sort_order
                category.is_active = True
                category.save(update_fields=["sort_order", "is_active"])

    def _seed_dishes(self, items: list[dict]) -> None:
        for item in items:
            category = Category.objects.get(name=item["category"])
            photo = item.get("photo", "")
            slug = item.get("slug") or (Path(photo).stem if photo else "")
            if not slug:
                continue
            defaults = {
                "category": category,
                "name": item["name"],
                "description": item.get("description", ""),
                "price": Decimal(item["price"]),
                "weight": item.get("weight", 0),
                "is_spicy": item.get("is_spicy", False),
                "is_vegetarian": item.get("is_vegetarian", False),
                "is_recommended": item.get("is_recommended", False),
                "is_active": True,
            }
            dish, _ = Dish.objects.update_or_create(slug=slug, defaults=defaults)
            dish.photo = photo if photo else ""
            dish.save()

    def _deactivate_dishes(self, names: list[str]) -> None:
        if not names:
            return
        Dish.objects.filter(name__in=names).delete()

    def _prune_dishes(self, items: list[dict]) -> None:
        keep_slugs = {item["slug"] for item in items if item.get("slug")}
        removed = 0
        for dish in Dish.objects.exclude(slug__in=keep_slugs):
            dish.delete()
            removed += 1
        if removed:
            self.stdout.write(f"Removed {removed} dish(es) not listed in manifest.")

    def _prune_categories(self, items: list[dict]) -> None:
        keep = {item["name"] for item in items}
        removed = 0
        hidden = 0
        for category in Category.objects.exclude(name__in=keep):
            if category.dishes.exists():
                category.is_active = False
                category.save(update_fields=["is_active"])
                hidden += 1
            else:
                category.delete()
                removed += 1
        if removed:
            self.stdout.write(f"Removed {removed} unused categor(ies).")
        if hidden:
            self.stdout.write(f"Hidden {hidden} obsolete categor(ies).")

    def _seed_gallery(self, items: list[dict]) -> None:
        for item in items:
            image = item["image"]
            title = item.get("title", "")
            obj, _ = GalleryImage.objects.update_or_create(
                title=title,
                defaults={
                    "image": image,
                    "category": item.get("category", GalleryImage.Category.INTERIOR),
                    "is_published": True,
                },
            )

    def _seed_events(self, items: list[dict]) -> None:
        now = timezone.now()
        for item in items:
            start = now + timedelta(days=item.get("days_from_now", 7))
            end = start + timedelta(hours=item.get("duration_hours", 2))
            event, created = Event.objects.get_or_create(
                title=item["title"],
                defaults={
                    "description": item.get("description", ""),
                    "date_start": start,
                    "date_end": end,
                    "price": Decimal(item["price"]) if item.get("price") else None,
                    "max_guests": item.get("max_guests", 0),
                    "is_published": True,
                },
            )
            photo = item.get("photo", "")
            if photo:
                event.photo = photo
                event.save(update_fields=["photo"])

    def _seed_tables(self, items: list[dict]) -> None:
        for item in items:
            Table.objects.update_or_create(
                number=item["number"],
                defaults={
                    "seats": item["seats"],
                    "location": item.get("location", Table.Location.HALL),
                    "is_active": item.get("is_active", True),
                },
            )

    def _prune_tables(self, items: list[dict]) -> None:
        keep = {item["number"] for item in items}
        if not keep:
            return
        removed = 0
        hidden = 0
        for table in Table.objects.exclude(number__in=keep):
            if table.bookings.exists():
                if table.is_active:
                    table.is_active = False
                    table.save(update_fields=["is_active"])
                    hidden += 1
            else:
                table.delete()
                removed += 1
        if removed:
            self.stdout.write(f"Removed {removed} table(s) not listed in manifest.")
        if hidden:
            self.stdout.write(f"Deactivated {hidden} obsolete table(s) with bookings.")
