#!/bin/sh
python manage.py migrate --no-input
python manage.py collectstatic --no-input
gunicorn optomcalc.wsgi:application --workers=2 --threads=4 --worker-class=gthread --bind :8000 --worker-tmp-dir /dev/shm
