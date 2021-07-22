FROM python:3.8-slim

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
	PYTHONDONTWRITEBYTECODE=1\
	PYTHONUNBUFFERED=1 \
	PYTHONHASHSEED=random \
	PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_DEFAULT_TIMEOUT=100

RUN pip install pipenv
COPY ./optomcalc/Pipfile ./optomcalc/Pipfile.lock /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./optomcalc /usr/src/

EXPOSE 8000
