"""Import ready photos from Desktop/ФОТО into assets/bundled/."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"C:\Users\dmekh\Desktop\ФОТО")
BUNDLED = ROOT / "assets" / "bundled"

SLIDES = [
    ("СТОЛ ВЕРХ.webp", "static/img/home-slider/slide-1.webp"),
    ("СТОЛ БОК.webp", "static/img/home-slider/slide-2.webp"),
    ("БЛЮДО СЛАЙДЕР.webp", "static/img/home-slider/slide-3.webp"),
]

GALLERY = [(f"ГАЛЛЕРЕЯ {i}.webp", f"media/gallery/gallery-{i:02d}.webp") for i in range(1, 11)]

DISHES = [
    {
        "slug": "odzhahuri-svinina",
        "sources": ["odzhahuri-svinina.webp"],
        "category": "Горячие блюда",
        "name": "Оджахури со свининой",
        "description": "Жареное мясо с картофелем, луком и специями.",
        "price": "590.00",
        "weight": 350,
        "is_recommended": True,
    },
    {
        "slug": "odzhahuri-govyadina",
        "sources": ["odzhahuri-govyadina.webp", "odzhakhuri s govyadinoy.webp"],
        "category": "Горячие блюда",
        "name": "Оджахури с говядиной",
        "description": "Сочная говядина с картофелем по домашнему рецепту.",
        "price": "620.00",
        "weight": 350,
    },
    {
        "slug": "zharkoe-semga",
        "sources": ["zharkoe-semga.webp", "zharkoye s semgoy.webp"],
        "category": "Горячие блюда",
        "name": "Жаркое с семгой",
        "description": "Нежная семга с овощами в ароматном соусе.",
        "price": "780.00",
        "weight": 320,
    },
    {
        "slug": "krevetki-chkmeruli",
        "sources": ["krevetki-chkmeruli.webp", "krevetki chkmeruli.webp"],
        "category": "Горячие блюда",
        "name": "Креветки чкмерули",
        "description": "Креветки в сливочно-чесночном соусе с сыром.",
        "price": "890.00",
        "weight": 280,
        "is_recommended": True,
    },
    {
        "slug": "shampinony-suluguni",
        "sources": [
            "shampinony-suluguni.webp",
            "Shampinony farshirovannyye s syrom suluguni.webp",
        ],
        "category": "Горячие блюда",
        "name": "Шампиньоны фаршированные с сулугуни",
        "description": "Запечённые шампиньоны с расплавленным сулугуни.",
        "price": "420.00",
        "weight": 250,
    },
    {
        "slug": "khatakhari",
        "sources": ["khatakhari.webp", "khatakhari.jpg"],
        "category": "Горячие блюда",
        "name": "Хачапури хатахтари",
        "description": "Хачапури с начинкой из яиц, сыра и масла.",
        "price": "510.00",
        "weight": 380,
    },
    {
        "slug": "khachapuri",
        "sources": ["khachapuri.webp", "khachapuri.jpg", "khachapuri-adjaruli.webp"],
        "category": "Горячие блюда",
        "name": "Хачапури по-аджарски",
        "description": "Лодочка из теста с сыром, яйцом и сливочным маслом.",
        "price": "550.00",
        "weight": 420,
        "is_recommended": True,
    },
    {
        "slug": "khachapuri-imeruli",
        "sources": ["khachapuri-imeruli.webp", "khachapuri-imeruli.jpg"],
        "category": "Горячие блюда",
        "name": "Хачапури по-имеретински",
        "description": "Круглый хачапури с сыром сулугуни внутри.",
        "price": "480.00",
        "weight": 350,
    },
    {
        "slug": "khinkali",
        "sources": ["khinkali.webp", "khinkali.jpg"],
        "category": "Горячие блюда",
        "name": "Хинкали с мясом",
        "description": "Классические грузинские пельмени с сочной мясной начинкой.",
        "price": "460.00",
        "weight": 300,
        "is_recommended": True,
    },
    {
        "slug": "satsivi-indejka",
        "sources": ["satsivi-indejka.webp", "Satsivi s indeykoy.webp"],
        "category": "Горячие блюда",
        "name": "Сациви с индейкой",
        "description": "Индейка в густом грузинском ореховом соусе.",
        "price": "480.00",
        "weight": 300,
    },
    {
        "slug": "satsivi",
        "sources": ["satsivi.webp", "satsivi.jpg"],
        "category": "Горячие блюда",
        "name": "Сациви",
        "description": "Курица в густом ореховом соусе по грузинскому рецепту.",
        "price": "450.00",
        "weight": 300,
    },
    {
        "slug": "adjapsandali",
        "sources": ["adjapsandali.webp", "Adzhapsandali.webp"],
        "category": "Горячие блюда",
        "name": "Аджапсандали",
        "description": "Тушёные баклажаны с перцем и томатами.",
        "price": "360.00",
        "weight": 260,
        "is_vegetarian": True,
    },
    {
        "slug": "badrijani-oreh",
        "sources": [
            "badrijani-oreh.webp",
            "Badridzhani s pashtetom iz gretskikh orekhov.webp",
        ],
        "category": "Горячие блюда",
        "name": "Бадриджани с паштетом из грецких орехов",
        "description": "Баклажаны с ореховой пастой и зеленью.",
        "price": "340.00",
        "weight": 220,
        "is_vegetarian": True,
    },
    {
        "slug": "badrijani",
        "sources": ["badrijani.webp", "badrijani.jpg"],
        "category": "Горячие блюда",
        "name": "Бадриджани",
        "description": "Маринованные баклажаны с чесноком и зеленью.",
        "price": "320.00",
        "weight": 200,
        "is_vegetarian": True,
    },
    {
        "slug": "baklazhan-syr",
        "sources": ["baklazhan-syr.webp", "baklazhan s syrom.webp"],
        "category": "Горячие блюда",
        "name": "Баклажан с сыром",
        "description": "Запечённый баклажан с сырной начинкой.",
        "price": "320.00",
        "weight": 240,
        "is_vegetarian": True,
    },
    {
        "slug": "lobio",
        "sources": ["lobio.webp", "lobio.jpg"],
        "category": "Горячие блюда",
        "name": "Лобио",
        "description": "Традиционная фасоль с ароматными специями.",
        "price": "320.00",
        "weight": 250,
        "is_vegetarian": True,
    },
    {
        "slug": "lobio-kakheti",
        "sources": ["lobio-kakheti.webp", "lobio-kakheti.jpg", "lobio po kakhetinski.jpg"],
        "category": "Горячие блюда",
        "name": "Лобио по-кахетински",
        "description": "Фасоль с ароматными специями и зеленью.",
        "price": "350.00",
        "weight": 280,
        "is_vegetarian": True,
    },
    {
        "slug": "mtsnili-bochka",
        "sources": [
            "mtsnili-bochka.webp",
            "Mtsnili iz bochki (kapusta po guriyski. ostryy perets. ogurtsy. cheremsha i dzhondzholi).webp",
        ],
        "category": "Горячие блюда",
        "name": "Мцниве из бочки",
        "description": "Ассорти из капусты, огурцов, перца и черемши.",
        "price": "290.00",
        "weight": 200,
    },
    {
        "slug": "phkali-assorti",
        "sources": ["phkali-assorti.webp", "Pkhaleuli iz svekly. shpinata i fasoli.webp"],
        "category": "Горячие блюда",
        "name": "Пхали из свеклы, шпината и фасоли",
        "description": "Традиционные пасты из овощей с орехами и специями.",
        "price": "380.00",
        "weight": 250,
        "is_vegetarian": True,
    },
    {
        "slug": "semga-tarhun",
        "sources": ["semga-tarhun.webp", "Semga slabosolenaya s tarkhunom.webp"],
        "category": "Горячие блюда",
        "name": "Семга слабосоленая с тархуном",
        "description": "Нежная семга с ароматом свежего тархуна.",
        "price": "560.00",
        "weight": 180,
    },
    {
        "slug": "suluguni-tomaty",
        "sources": ["suluguni-tomaty.webp", "suluguni s tomatami.webp"],
        "category": "Горячие блюда",
        "name": "Сулугуни с томатами",
        "description": "Сыр сулугуни с свежими томатами и зеленью.",
        "price": "410.00",
        "weight": 220,
        "is_vegetarian": True,
    },
    {
        "slug": "tarhun",
        "sources": ["tarhun.webp", "tarhun_v_stakane.webp"],
        "category": "Напитки",
        "name": "Тархун",
        "description": "Освежающий лимонад из тархуна.",
        "price": "220.00",
        "weight": 300,
    },
    {
        "slug": "kola",
        "sources": ["kola.webp", "Kola.webp"],
        "category": "Напитки",
        "name": "Кола",
        "description": "Классический газированный напиток.",
        "price": "180.00",
        "weight": 330,
    },
    {
        "slug": "mandarin-marakuja",
        "sources": [
            "МАНдарин маракуйя2.webp",
            "mandarin-marakuja.webp",
            "mandarin marakuyya.webp",
        ],
        "category": "Напитки",
        "name": "Мандарин-маракуйя",
        "description": "Фруктовый микс из мандарина и маракуйи.",
        "price": "240.00",
        "weight": 300,
    },
]

EVENT = {
    "src": "krevetki chkmeruli.webp",
    "dest": "media/events/wine-evening.webp",
}

PHOTO_EXTENSIONS = (".webp", ".jpg", ".jpeg", ".png")


def _source_index() -> dict[str, Path]:
    index: dict[str, Path] = {}
    if not SOURCE.is_dir():
        return index
    for candidate in SOURCE.iterdir():
        if candidate.is_file():
            index[candidate.name.casefold()] = candidate
    return index


def _resolve_source_name(src_name: str, index: dict[str, Path]) -> Path | None:
    direct = index.get(src_name.casefold())
    if direct is not None:
        return direct
    direct_path = SOURCE / src_name
    if direct_path.is_file():
        return direct_path
    return None


def _resolve_dish_photo(slug: str, sources: list[str], index: dict[str, Path]) -> Path | None:
    for name in sources:
        found = _resolve_source_name(name, index)
        if found is not None:
            return found
    for ext in PHOTO_EXTENSIONS:
        found = _resolve_source_name(f"{slug}{ext}", index)
        if found is not None:
            return found
    bundled = BUNDLED / "media" / "menu" / f"{slug}{PHOTO_EXTENSIONS[0]}"
    if bundled.is_file() and bundled.stat().st_size > 50_000:
        return bundled
    return None


def copy_path(src: Path, dest_rel: str) -> None:
    dest = BUNDLED / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def copy_file(src_name: str, dest_rel: str) -> None:
    index = _source_index()
    src = _resolve_source_name(src_name, index)
    if src is None:
        raise FileNotFoundError(f"Missing photo: {SOURCE / src_name}")
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
        for dest in copied_photos:
            if Path(dest).stem == slug:
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
    if not SOURCE.is_dir():
        raise SystemExit(f"Photo folder not found: {SOURCE}")

    copied_photos: set[str] = set()
    index = _source_index()
    missing: list[str] = []

    for src_name, dest_rel in SLIDES + GALLERY:
        copy_file(src_name, dest_rel)

    for item in DISHES:
        slug = item["slug"]
        src = _resolve_dish_photo(slug, item.get("sources", []), index)
        if src is None:
            missing.append(item["name"])
            continue
        dest_rel = f"media/menu/{slug}{src.suffix.lower()}"
        copy_path(src, dest_rel)
        copied_photos.add(dest_rel)

    copy_file(EVENT["src"], EVENT["dest"])

    manifest = build_manifest(copied_photos)
    (BUNDLED / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    imported = len(SLIDES) + len(GALLERY) + len(copied_photos) + 1
    print(f"Imported {imported} photos into {BUNDLED}")
    if missing:
        print("Missing photos for:", ", ".join(missing))


if __name__ == "__main__":
    main()
