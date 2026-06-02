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
        "src": "odzhahuri-svinina.webp",
        "dest": "media/menu/odzhahuri-svinina.webp",
        "category": "Горячие блюда",
        "name": "Оджахури со свининой",
        "description": "Жареное мясо с картофелем, луком и специями.",
        "price": "590.00",
        "weight": 350,
        "is_recommended": True,
    },
    {
        "src": "odzhakhuri s govyadinoy.webp",
        "dest": "media/menu/odzhahuri-govyadina.webp",
        "category": "Горячие блюда",
        "name": "Оджахури с говядиной",
        "description": "Сочная говядина с картофелем по домашнему рецепту.",
        "price": "620.00",
        "weight": 350,
    },
    {
        "src": "zharkoye s semgoy.webp",
        "dest": "media/menu/zharkoe-semga.webp",
        "category": "Горячие блюда",
        "name": "Жаркое с семгой",
        "description": "Нежная семга с овощами в ароматном соусе.",
        "price": "780.00",
        "weight": 320,
    },
    {
        "src": "krevetki chkmeruli.webp",
        "dest": "media/menu/krevetki-chkmeruli.webp",
        "category": "Горячие блюда",
        "name": "Креветки чкмерули",
        "description": "Креветки в сливочно-чесночном соусе с сыром.",
        "price": "890.00",
        "weight": 280,
        "is_recommended": True,
    },
    {
        "src": "Shampinony farshirovannyye s syrom suluguni.webp",
        "dest": "media/menu/shampinony-suluguni.webp",
        "category": "Горячие блюда",
        "name": "Шампиньоны фаршированные с сулугуни",
        "description": "Запечённые шампиньоны с расплавленным сулугуни.",
        "price": "420.00",
        "weight": 250,
    },
    {
        "src": "ХАТАХТАРИ.webp",
        "dest": "media/menu/khatakhari.webp",
        "category": "Выпечка",
        "name": "Хачапури хатахтари",
        "description": "Хачапури с начинкой из яиц, сыра и масла.",
        "price": "510.00",
        "weight": 380,
    },
    {
        "src": "Satsivi s indeykoy.webp",
        "dest": "media/menu/satsivi-indejka.webp",
        "category": "Горячие блюда",
        "name": "Сациви с индейкой",
        "description": "Индейка в густом грузинском ореховом соусе.",
        "price": "480.00",
        "weight": 300,
    },
    {
        "src": "Adzhapsandali.webp",
        "dest": "media/menu/adjapsandali.webp",
        "category": "Закуски",
        "name": "Аджапсандали",
        "description": "Тушёные баклажаны с перцем и томатами.",
        "price": "360.00",
        "weight": 260,
        "is_vegetarian": True,
    },
    {
        "src": "Badridzhani s pashtetom iz gretskikh orekhov.webp",
        "dest": "media/menu/badrijani-oreh.webp",
        "category": "Закуски",
        "name": "Бадриджани с паштетом из грецких орехов",
        "description": "Баклажаны с ореховой пастой и зеленью.",
        "price": "340.00",
        "weight": 220,
        "is_vegetarian": True,
    },
    {
        "src": "baklazhan s syrom.webp",
        "dest": "media/menu/baklazhan-syr.webp",
        "category": "Закуски",
        "name": "Баклажан с сыром",
        "description": "Запечённый баклажан с сырной начинкой.",
        "price": "320.00",
        "weight": 240,
        "is_vegetarian": True,
    },
    {
        "src": "lobio po kakhetinski.jpg",
        "dest": "media/menu/lobio-kakheti.jpg",
        "category": "Закуски",
        "name": "Лобио по-кахетински",
        "description": "Фасоль с ароматными специями и зеленью.",
        "price": "350.00",
        "weight": 280,
        "is_vegetarian": True,
    },
    {
        "src": "Mtsnili iz bochki (kapusta po guriyski. ostryy perets. ogurtsy. cheremsha i dzhondzholi).webp",
        "dest": "media/menu/mtsnili-bochka.webp",
        "category": "Закуски",
        "name": "Мцниве из бочки",
        "description": "Ассорти из капусты, огурцов, перца и черемши.",
        "price": "290.00",
        "weight": 200,
    },
    {
        "src": "Pkhaleuli iz svekly. shpinata i fasoli.webp",
        "dest": "media/menu/phkali-assorti.webp",
        "category": "Закуски",
        "name": "Пхали из свеклы, шпината и фасоли",
        "description": "Традиционные пасты из овощей с орехами и специями.",
        "price": "380.00",
        "weight": 250,
        "is_vegetarian": True,
    },
    {
        "src": "Semga slabosolenaya s tarkhunom.webp",
        "dest": "media/menu/semga-tarhun.webp",
        "category": "Закуски",
        "name": "Семга слабосоленая с тархуном",
        "description": "Нежная семга с ароматом свежего тархуна.",
        "price": "560.00",
        "weight": 180,
    },
    {
        "src": "suluguni s tomatami.webp",
        "dest": "media/menu/suluguni-tomaty.webp",
        "category": "Закуски",
        "name": "Сулугуни с томатами",
        "description": "Сыр сулугуни с свежими томатами и зеленью.",
        "price": "410.00",
        "weight": 220,
        "is_vegetarian": True,
    },
    {
        "src": "tarhun_v_stakane.webp",
        "dest": "media/menu/tarhun.webp",
        "category": "Напитки",
        "name": "Тархун",
        "description": "Освежающий лимонад из тархуна.",
        "price": "220.00",
        "weight": 300,
    },
    {
        "src": "Kola.webp",
        "dest": "media/menu/kola.webp",
        "category": "Напитки",
        "name": "Кола",
        "description": "Классический газированный напиток.",
        "price": "180.00",
        "weight": 330,
    },
    {
        "src": "mandarin marakuyya.webp",
        "dest": "media/menu/mandarin-marakuja.webp",
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


def _resolve_source(src_name: str) -> Path:
    direct = SOURCE / src_name
    if direct.is_file():
        return direct
    wanted = src_name.casefold()
    for candidate in SOURCE.iterdir():
        if candidate.is_file() and candidate.name.casefold() == wanted:
            return candidate
    raise FileNotFoundError(f"Missing photo: {SOURCE / src_name}")


def copy_file(src_name: str, dest_rel: str) -> None:
    src = _resolve_source(src_name)
    dest = BUNDLED / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def build_manifest() -> dict:
    categories = [
        {"name": "Горячие блюда", "sort_order": 1},
        {"name": "Выпечка", "sort_order": 2},
        {"name": "Закуски", "sort_order": 3},
        {"name": "Напитки", "sort_order": 4},
    ]
    dishes = []
    for item in DISHES:
        dishes.append(
            {
                "category": item["category"],
                "name": item["name"],
                "slug": Path(item["dest"]).stem,
                "description": item["description"],
                "price": item["price"],
                "weight": item["weight"],
                "photo": item["dest"].replace("media/", "", 1),
                **{k: item[k] for k in ("is_recommended", "is_vegetarian", "is_spicy") if k in item},
            }
        )
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
        "deactivate_dishes": [
            "Хачапури по-аджарски",
            "Хинкали с мясом",
            "Лобио",
            "Сациви",
            "Хачапури по-имеретински",
            "Бадриджани",
        ],
    }


def main() -> None:
    if not SOURCE.is_dir():
        raise SystemExit(f"Photo folder not found: {SOURCE}")

    for src_name, dest_rel in SLIDES + GALLERY:
        copy_file(src_name, dest_rel)

    for item in DISHES:
        copy_file(item["src"], item["dest"])

    copy_file(EVENT["src"], EVENT["dest"])

    manifest = build_manifest()
    (BUNDLED / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Imported {len(SLIDES) + len(GALLERY) + len(DISHES) + 1} photos into {BUNDLED}")


if __name__ == "__main__":
    main()
