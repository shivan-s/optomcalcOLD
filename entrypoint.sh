#!/bin/sh

poetry run python manage.py migrate --no-input
poetry run python manage.py collectstatic --no-input

poetry run gunicorn optomcalc.wsgi:application -w 2 -b 0.0.0.0:8000 --timeout 120
