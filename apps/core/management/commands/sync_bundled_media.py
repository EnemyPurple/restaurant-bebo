from __future__ import annotations

import json
import shutil
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.events.models import Event
from apps.gallery.models import GalleryImage
from apps.menu.models import Category, Dish


class Command(BaseCommand):
    help = "Copy bundled images into static/media and ensure demo DB records exist"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        bundled_root = settings.BASE_DIR / "assets" / "bundled"
        manifest_path = bundled_root / "manifest.json"
        if not bundled_root.exists():
            self.stdout.write(self.style.WARNING("No assets/bundled folder found, skipping."))
            return

        copied = self._copy_tree(bundled_root / "static", settings.BASE_DIR / "static", overwrite=True)
        copied += self._copy_tree(bundled_root / "media", settings.MEDIA_ROOT, overwrite=True)
        self.stdout.write(f"Synced {copied} bundled file(s) to static/media.")

        if not manifest_path.exists():
            return

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self._seed_categories(manifest.get("categories", []))
        self._deactivate_dishes(manifest.get("deactivate_dishes", []))
        dishes = manifest.get("dishes", [])
        self._seed_dishes(dishes)
        self._prune_dishes(dishes)
        self._seed_gallery(manifest.get("gallery", []))
        self._seed_events(manifest.get("events", []))
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
            Category.objects.get_or_create(
                name=item["name"],
                defaults={"sort_order": item.get("sort_order", 0), "is_active": True},
            )

    def _seed_dishes(self, items: list[dict]) -> None:
        for item in items:
            category = Category.objects.get(name=item["category"])
            photo = item.get("photo", "")
            slug = item.get("slug") or (Path(photo).stem if photo else "")
            defaults = {
                "description": item.get("description", ""),
                "price": Decimal(item["price"]),
                "weight": item.get("weight", 0),
                "is_spicy": item.get("is_spicy", False),
                "is_vegetarian": item.get("is_vegetarian", False),
                "is_recommended": item.get("is_recommended", False),
                "is_active": True,
            }
            if slug:
                Dish.objects.filter(category=category, name=item["name"]).exclude(slug=slug).delete()
                Dish.objects.filter(slug=slug).exclude(category=category, name=item["name"]).delete()
                defaults["slug"] = slug
            dish, _ = Dish.objects.update_or_create(
                category=category,
                name=item["name"],
                defaults=defaults,
            )
            if slug and dish.slug != slug:
                dish.slug = slug
            if photo:
                dish.photo = photo
            dish.save()

    def _deactivate_dishes(self, names: list[str]) -> None:
        if not names:
            return
        Dish.objects.filter(name__in=names).delete()

    def _prune_dishes(self, items: list[dict]) -> None:
        keep = {(item["category"], item["name"]) for item in items}
        removed = 0
        for dish in Dish.objects.select_related("category"):
            if (dish.category.name, dish.name) not in keep:
                dish.delete()
                removed += 1
        if removed:
            self.stdout.write(f"Removed {removed} dish(es) not listed in manifest.")

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
