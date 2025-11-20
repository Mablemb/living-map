#!/usr/bin/env sh
set -e

echo "==> Running migrations"
python manage.py migrate --noinput

echo "==> Ensuring media/static directories exist"
mkdir -p media staticfiles

echo "==> Django settings quick debug"
python - <<'PY'
import os
from django.conf import settings
print("DEBUG=", settings.DEBUG)
print("ALLOWED_HOSTS=", settings.ALLOWED_HOSTS)
print("AWS_STORAGE_BUCKET_NAME=", os.getenv('AWS_STORAGE_BUCKET_NAME'))
print("AWS_S3_CUSTOM_DOMAIN=", os.getenv('AWS_S3_CUSTOM_DOMAIN'))
PY

echo "==> Starting gunicorn"
gunicorn setup.wsgi:application --bind 0.0.0.0:${PORT:-8000}
