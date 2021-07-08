#! /bin/bash
if [ -z "$1" ]
then pipenv run python3 manage.py runserver 8000
else pipenv run python3 manage.py $1 $2 $3
fi
