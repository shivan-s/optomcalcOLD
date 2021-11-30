#!/bin/sh
pipenv run python manage.py migrate --no-input
pipenv run python manage.py collectstatic --no-input
pipenv run gunicorn config.wsgi:application --workers=2 --threads=4 --worker-class=gthread --bind :8000 --worker-tmp-dir /dev/shm
