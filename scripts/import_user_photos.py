"""Import ready photos from Desktop/ФОТО or media/menu into assets/bundled/."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"C:\Users\dmekh\Desktop\ФОТО")
LOCAL_MENU = ROOT / "media" / "menu"
BUNDLED = ROOT / "assets" / "bundled"

SLIDES = [
    ("СТОЛ ВЕРХ.webp", "static/img/home-slider/slide-1.webp"),
    ("СТОЛ БОК.webp", "static/img/home-slider/slide-2.webp"),
    ("БЛЮДО СЛАЙДЕР.webp", "static/img/home-slider/slide-3.webp"),
]

GALLERY = [(f"ГАЛЛЕРЕЯ {i}.webp", f"media/gallery/gallery-{i:02d}.webp") for i in range(1, 11)]

DISHES = [
    {
        "slug": "adjapsandali",
        "category": "Горячие блюда",
        "name": "Аджапсандали",
        "description": "Тушёные баклажаны с перцем и томатами.",
        "price": "360.00",
        "weight": 260,
        "is_vegetarian": True,
    },
    {
        "slug": "badrijani-oreh",
        "category": "Горячие блюда",
        "name": "Бадриджани с паштетом из грецких орехов",
        "description": "Баклажаны с ореховой пастой и зеленью.",
        "price": "340.00",
        "weight": 220,
        "is_vegetarian": True,
    },
    {
        "slug": "baklazhan-syr",
        "category": "Горячие блюда",
        "name": "Баклажан с сыром",
        "description": "Запечённый баклажан с сырной начинкой.",
        "price": "320.00",
        "weight": 240,
        "is_vegetarian": True,
    },
    {
        "slug": "zharkoe-semga",
        "category": "Горячие блюда",
        "name": "Жаркое с семгой",
        "description": "Нежная семга с овощами в ароматном соусе.",
        "price": "780.00",
        "weight": 320,
    },
    {
        "slug": "krevetki-chkmeruli",
        "category": "Горячие блюда",
        "name": "Креветки чкмерули",
        "description": "Креветки в сливочно-чесночном соусе с сыром.",
        "price": "890.00",
        "weight": 280,
        "is_recommended": True,
    },
    {
        "slug": "lobio-kakheti",
        "category": "Горячие блюда",
        "name": "Лобио по-кахетински",
        "description": "Фасоль с ароматными специями и зеленью.",
        "price": "350.00",
        "weight": 280,
        "is_vegetarian": True,
    },
    {
        "slug": "mtsnili-bochka",
        "category": "Горячие блюда",
        "name": "Мцнили из бочки",
        "description": "Ассорти из капусты, огурцов, перца и черемши.",
        "price": "290.00",
        "weight": 200,
        "is_spicy": True,
    },
    {
        "slug": "odzhahuri-govyadina",
        "category": "Горячие блюда",
        "name": "Оджахури с говядиной",
        "description": "Сочная говядина с картофелем по домашнему рецепту.",
        "price": "620.00",
        "weight": 350,
    },
    {
        "slug": "odzhahuri-svinina",
        "category": "Горячие блюда",
        "name": "Оджахури со свининой",
        "description": "Жареное мясо с картофелем, луком и специями.",
        "price": "590.00",
        "weight": 350,
        "is_recommended": True,
    },
    {
        "slug": "phkali-assorti",
        "category": "Горячие блюда",
        "name": "Пхалеули из свеклы, шпината и фасоли",
        "description": "Традиционные пасты из овощей с орехами и специями.",
        "price": "380.00",
        "weight": 250,
        "is_spicy": True,
        "is_vegetarian": True,
    },
    {
        "slug": "satsivi-indejka",
        "category": "Горячие блюда",
        "name": "Сациви с индейкой",
        "description": "Индейка в густом грузинском ореховом соусе.",
        "price": "480.00",
        "weight": 300,
    },
    {
        "slug": "semga-tarhun",
        "category": "Горячие блюда",
        "name": "Семга слабосоленая с тархуном",
        "description": "Нежная семга с ароматом свежего тархуна.",
        "price": "560.00",
        "weight": 180,
    },
    {
        "slug": "suluguni-tomaty",
        "category": "Горячие блюда",
        "name": "Сулугуни с томатами",
        "description": "Сыр сулугуни с свежими томатами и зеленью.",
        "price": "410.00",
        "weight": 220,
        "is_vegetarian": True,
    },
    {
        "slug": "khachapuri",
        "category": "Горячие блюда",
        "name": "Хачапури по-аджарски",
        "description": "Лодочка из теста с сыром, яйцом и сливочным маслом.",
        "price": "550.00",
        "weight": 420,
        "is_recommended": True,
    },
    {
        "slug": "khachapuri-imeruli",
        "category": "Горячие блюда",
        "name": "Хачапури по-имеретински",
        "description": "Круглый хачапури с сыром сулугуни внутри.",
        "price": "480.00",
        "weight": 350,
    },
    {
        "slug": "shampinony-suluguni",
        "category": "Горячие блюда",
        "name": "Шампиньоны фаршированные с сулугуни",
        "description": "Запечённые шампиньоны с расплавленным сулугуни.",
        "price": "420.00",
        "weight": 250,
    },
    {
        "slug": "kola",
        "category": "Напитки",
        "name": "Кола",
        "description": "Классический газированный напиток.",
        "price": "180.00",
        "weight": 330,
    },
    {
        "slug": "fejhoa-lichi",
        "category": "Напитки",
        "name": "Фейхоа личи",
        "description": "Фруктовый микс фейхоа личи.",
        "price": "240.00",
        "weight": 300,
    },
    {
        "slug": "natahtari",
        "category": "Напитки",
        "name": "Натахтари",
        "description": "Освежающий лимонад.",
        "price": "330.00",
        "weight": 330,
    },
    {
        "slug": "tarhun",
        "category": "Напитки",
        "name": "Тархун",
        "description": "Освежающий лимонад из тархуна.",
        "price": "220.00",
        "weight": 300,
    },
]

EVENT = {
    "src": "krevetki chkmeruli.webp",
    "dest": "media/events/wine-evening.webp",
}

PHOTO_EXTENSIONS = (".webp", ".jpg", ".jpeg", ".png")
FILENAME_ALIASES = {
    "cola": "kola",
    "tarhun_v_stakane": "tarhun",
}
DISH_PHOTO_FILES = {
    "kola": "cola.webp",
}


def _photo_roots() -> list[Path]:
    roots = [LOCAL_MENU]
    if SOURCE.is_dir():
        roots.append(SOURCE)
    return roots


def _source_index() -> dict[str, Path]:
    index: dict[str, Path] = {}
    for root in _photo_roots():
        if not root.is_dir():
            continue
        for candidate in root.iterdir():
            if not candidate.is_file():
                continue
            slug = FILENAME_ALIASES.get(candidate.stem, candidate.stem)
            key = f"{slug}{candidate.suffix.lower()}".casefold()
            if key not in index:
                index[key] = candidate
    return index


def _resolve_source_name(src_name: str, index: dict[str, Path]) -> Path | None:
    slug = FILENAME_ALIASES.get(Path(src_name).stem, Path(src_name).stem)
    ext = Path(src_name).suffix
    return index.get(f"{slug}{ext}".casefold())


def _resolve_dish_photo(slug: str, index: dict[str, Path]) -> Path | None:
    if slug == "kola":
        cola = LOCAL_MENU / "cola.webp"
        if cola.is_file():
            return cola
    for ext in PHOTO_EXTENSIONS:
        found = index.get(f"{slug}{ext}".casefold())
        if found is not None:
            return found
    return None


def copy_path(src: Path, dest_rel: str) -> None:
    dest = BUNDLED / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def copy_file(src_name: str, dest_rel: str, index: dict[str, Path]) -> None:
    src = _resolve_source_name(src_name, index)
    if src is None:
        for root in _photo_roots():
            direct = root / src_name
            if direct.is_file():
                src = direct
                break
    if src is None:
        raise FileNotFoundError(f"Missing photo: {src_name}")
    copy_path(src, dest_rel)


def build_manifest(copied_photos: set[str]) -> dict:
    categories = [
        {"name": "Горячие блюда", "sort_order": 1},
        {"name": "Напитки", "sort_order": 2},
    ]
    dishes = []
    for item in DISHES:
        slug = item["slug"]
        rel_photo = ""
        photo_file = DISH_PHOTO_FILES.get(slug, f"{slug}.webp")
        photo_stem = Path(photo_file).stem
        for dest in copied_photos:
            if Path(dest).stem in {slug, photo_stem}:
                rel_photo = dest.replace("media/", "", 1)
                break
        entry = {
            "category": item["category"],
            "name": item["name"],
            "slug": slug,
            "description": item["description"],
            "price": item["price"],
            "weight": item["weight"],
            **{k: item[k] for k in ("is_recommended", "is_vegetarian", "is_spicy") if k in item},
        }
        if rel_photo:
            entry["photo"] = rel_photo
        dishes.append(entry)
    gallery = [
        {
            "title": f"Ресторан «Бебо» — фото {i}",
            "image": f"gallery/gallery-{i:02d}.webp",
            "category": "interior" if i <= 7 else "food",
        }
        for i in range(1, 11)
    ]
    events = [
        {
            "title": "Вечер грузинской кухни",
            "description": "Авторское меню, живая музыка и атмосфера настоящей Грузии.",
            "photo": "events/wine-evening.webp",
            "days_from_now": 14,
            "duration_hours": 3,
            "price": "1500.00",
            "max_guests": 40,
        }
    ]
    return {
        "categories": categories,
        "dishes": dishes,
        "gallery": gallery,
        "events": events,
        "deactivate_dishes": [],
    }


def main() -> None:
    copied_photos: set[str] = set()
    index = _source_index()
    missing: list[str] = []

    if SOURCE.is_dir():
        for src_name, dest_rel in SLIDES + GALLERY:
            copy_file(src_name, dest_rel, index)
        copy_file(EVENT["src"], EVENT["dest"], index)

    menu_dir = BUNDLED / "media" / "menu"
    menu_dir.mkdir(parents=True, exist_ok=True)

    for item in DISHES:
        slug = item["slug"]
        src = _resolve_dish_photo(slug, index)
        if src is None:
            missing.append(item["name"])
            continue
        photo_name = DISH_PHOTO_FILES.get(slug, f"{slug}{src.suffix.lower()}")
        dest_rel = f"media/menu/{photo_name}"
        copy_path(src, dest_rel)
        copied_photos.add(dest_rel)

    manifest = build_manifest(copied_photos)
    (BUNDLED / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Menu: {len(DISHES)} dishes, {len(copied_photos)} with photos")
    if missing:
        print("Missing photos for:", ", ".join(missing))


if __name__ == "__main__":
    main()
