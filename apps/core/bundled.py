from __future__ import annotations

import io
import json
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management import call_command

DB_SNAPSHOT_NAME = "db.json"

# Все прикладные данные для деплоя (без sessions, permissions, logentry).
DUMP_LABELS = [
    "auth.user",
    "sites",
    "menu",
    "booking",
    "events",
    "gallery",
    "contacts",
    "reviews",
    "newsletter",
    "users",
]


def bundled_root() -> Path:
    return settings.BASE_DIR / "assets" / "bundled"


def db_snapshot_path() -> Path:
    return bundled_root() / DB_SNAPSHOT_NAME


def copy_media_to_bundled() -> int:
    src = Path(settings.MEDIA_ROOT)
    dst = bundled_root() / "media"
    if not src.is_dir():
        return 0
    copied = 0
    for file_path in src.rglob("*"):
        if not file_path.is_file():
            continue
        rel = file_path.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, target)
        copied += 1
    return copied


def export_db_snapshot() -> int:
    path = db_snapshot_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    buffer = io.StringIO()
    call_command(
        "dumpdata",
        *DUMP_LABELS,
        natural_foreign=True,
        natural_primary=True,
        indent=2,
        stdout=buffer,
    )
    payload = buffer.getvalue()
    path.write_text(payload if payload.endswith("\n") else payload + "\n", encoding="utf-8")
    return len(json.loads(payload))


def restore_db_snapshot() -> int:
    path = db_snapshot_path()
    if not path.is_file():
        raise FileNotFoundError(f"Missing DB snapshot: {path}")
    call_command("flush", interactive=False, verbosity=0)
    buffer = io.StringIO()
    call_command("loaddata", str(path), verbosity=1, stdout=buffer)
    loaded = 0
    for line in buffer.getvalue().splitlines():
        if "Installed" in line:
            try:
                loaded = int(line.split("Installed")[-1].strip().split()[0])
            except (IndexError, ValueError):
                pass
    return loaded
