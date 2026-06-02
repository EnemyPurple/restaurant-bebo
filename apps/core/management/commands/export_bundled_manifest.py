from __future__ import annotations

import json
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.menu.models import Category, Dish


class Command(BaseCommand):
    help = "Export active menu from DB into assets/bundled/manifest.json and copy dish photos"

    def handle(self, *args, **options):
        bundled_root = settings.BASE_DIR / "assets" / "bundled"
        manifest_path = bundled_root / "manifest.json"
        menu_dest = bundled_root / "media" / "menu"
        menu_dest.mkdir(parents=True, exist_ok=True)

        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        else:
            manifest = {"gallery": [], "events": [], "deactivate_dishes": []}

        categories = []
        for category in Category.objects.filter(is_active=True).order_by("sort_order", "name"):
            categories.append({"name": category.name, "sort_order": category.sort_order})

        dishes = []
        copied = 0
        for dish in Dish.objects.filter(is_active=True).select_related("category").order_by(
            "category__sort_order", "name"
        ):
            entry = {
                "category": dish.category.name,
                "name": dish.name,
                "slug": dish.slug,
                "description": dish.description,
                "price": f"{dish.price:.2f}",
                "weight": dish.weight,
            }
            if dish.is_recommended:
                entry["is_recommended"] = True
            if dish.is_vegetarian:
                entry["is_vegetarian"] = True
            if dish.is_spicy:
                entry["is_spicy"] = True

            photo = str(dish.photo or "").strip()
            if photo:
                rel = photo.replace("\\", "/")
                if rel.startswith("menu/"):
                    rel = rel[5:]
                src = settings.MEDIA_ROOT / "menu" / Path(rel).name
                if not src.is_file():
                    src = settings.MEDIA_ROOT / rel
                if src.is_file():
                    dest_name = Path(rel).name
                    shutil.copy2(src, menu_dest / dest_name)
                    entry["photo"] = f"menu/{dest_name}"
                    copied += 1
            dishes.append(entry)

        manifest["categories"] = categories
        manifest["dishes"] = dishes
        manifest.setdefault("deactivate_dishes", [])

        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Exported {len(categories)} categor(ies), {len(dishes)} dish(es), "
                f"{copied} photo(s) → {manifest_path.relative_to(settings.BASE_DIR)}"
            )
        )
