"""One-off script: generate demo images into assets/bundled/. Run from project root."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BUNDLED = ROOT / "assets" / "bundled"


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ("arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_image(path: Path, size: tuple[int, int], bg: tuple[int, int, int], title: str, subtitle: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", size, bg)
    draw = ImageDraw.Draw(img)
    w, h = size
    draw.rectangle([0, h - 8, w, h], fill=(240, 209, 160))
    font_l = _font(52 if w >= 1000 else 28)
    font_s = _font(28 if w >= 1000 else 16)
    draw.text((w // 2, h // 2 - (20 if subtitle else 0)), title, fill=(255, 255, 255), anchor="mm", font=font_l)
    if subtitle:
        draw.text((w // 2, h // 2 + 48), subtitle, fill=(240, 209, 160), anchor="mm", font=font_s)
    img.save(path, quality=88)


def main() -> None:
    slides = [
        ("static/img/home-slider/slide-1.png", (1920, 1080), (92, 26, 26), "Ресторан «Бебо»", "Грузинская кухня"),
        ("static/img/home-slider/slide-2.png", (1920, 1080), (120, 72, 24), "Хачапури и хинкали", "Свежая выпечка"),
        ("static/img/home-slider/slide-3.png", (1920, 1080), (34, 88, 54), "Уютный зал", "Йошкар-Ола"),
    ]
    menu = [
        ("media/menu/khachapuri.jpg", (800, 600), (180, 120, 40), "Хачапури по-аджарски"),
        ("media/menu/khinkali.jpg", (800, 600), (140, 90, 50), "Хинкали с мясом"),
        ("media/menu/lobio.jpg", (800, 600), (60, 110, 60), "Лобио"),
        ("media/menu/satsivi.jpg", (800, 600), (200, 160, 80), "Сatsivi"),
        ("media/menu/khachapuri-imeruli.jpg", (800, 600), (160, 100, 30), "Хачапури по-имеретински"),
        ("media/menu/badrijani.jpg", (800, 600), (80, 130, 70), "Бадриджани"),
    ]
    gallery = [
        ("media/gallery/interior-1.jpg", (1200, 900), (50, 45, 42), "Интерьер зала"),
        ("media/gallery/interior-2.jpg", (1200, 900), (65, 50, 45), "VIP-зона"),
        ("media/gallery/food-1.jpg", (1200, 900), (130, 85, 35), "Блюда шефа"),
        ("media/gallery/event-1.jpg", (1200, 900), (90, 35, 35), "Вечер живой музыки"),
    ]
    events = [
        ("media/events/wine-evening.jpg", (1000, 700), (70, 25, 35), "Вечер грузинского вина"),
    ]

    for rel, size, bg, title, *rest in slides + menu + gallery + events:
        subtitle = rest[0] if rest else ""
        make_image(BUNDLED / rel, size, bg, title, subtitle)

    print(f"Generated bundled images in {BUNDLED}")


if __name__ == "__main__":
    main()
