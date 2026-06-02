#!/usr/bin/env bash
set -euo pipefail

pip install -r requirements/prod.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py sync_bundled_media

if [ -n "${ADMIN_USERNAME:-}" ] && [ -n "${ADMIN_PASSWORD:-}" ]; then
  python manage.py ensure_admin --username "$ADMIN_USERNAME" --password "$ADMIN_PASSWORD"
fi
