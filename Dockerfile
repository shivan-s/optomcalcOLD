FROM python:slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1\
  PYTHONUNBUFFERED 1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.6

RUN pip install --upgrade pip \
	&& pip install "poetry==$POETRY_VERSION"


COPY poetry.lock pyproject.toml /optomcalc/

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY ./entrypoint.sh .

COPY . . 

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
