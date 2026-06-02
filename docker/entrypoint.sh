#!/usr/bin/env sh
set -e

python manage.py migrate --noinput
python manage.py sync_bundled_media
python manage.py collectstatic --noinput

exec "$@"

