from __future__ import annotations

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Backup PostgreSQL DB + media folder"

    def add_arguments(self, parser):
        parser.add_argument("--output-dir", default="backups", help="Directory to place backups")

    def handle(self, *args, **options):
        out_dir = Path(options["output_dir"]).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        db_name = settings.DATABASES["default"]["NAME"]
        db_user = settings.DATABASES["default"]["USER"]
        db_host = settings.DATABASES["default"]["HOST"]
        db_port = str(settings.DATABASES["default"]["PORT"])
        db_pass = settings.DATABASES["default"]["PASSWORD"]

        dump_path = out_dir / f"db_{db_name}_{ts}.sql"
        env = os.environ.copy()
        if db_pass:
            env["PGPASSWORD"] = db_pass

        self.stdout.write(f"Dumping DB to {dump_path} ...")
        subprocess.check_call(
            ["pg_dump", "-h", db_host, "-p", db_port, "-U", db_user, "-d", db_name, "-f", str(dump_path)],
            env=env,
        )

        media_src = Path(settings.MEDIA_ROOT)
        if media_src.exists():
            media_dst = out_dir / f"media_{ts}"
            self.stdout.write(f"Copying media to {media_dst} ...")
            shutil.copytree(media_src, media_dst, dirs_exist_ok=True)

        self.stdout.write(self.style.SUCCESS("Backup completed."))

