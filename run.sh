#! /bin/bash
if [ -z "$1" ]
then poetry run python3 manage.py runserver 8000
else poetry run python3 manage.py $1 $2 $3
fi
