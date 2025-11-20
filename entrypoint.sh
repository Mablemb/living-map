#!/usr/bin/env sh
set -e

echo "==> Running migrations"
python manage.py migrate --noinput

echo "==> Ensuring media/static directories exist"
mkdir -p media staticfiles

echo "==> Starting gunicorn"
gunicorn setup.wsgi:application --bind 0.0.0.0:${PORT:-8000}
