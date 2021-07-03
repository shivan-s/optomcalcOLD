FROM ubuntu:focal

RUN : \
	&& apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		python3 \
		pip \
	&& pip install 'poetry==1.1.6'

RUN mkdir -p /home/shivan/optomcalc/

WORKDIR home/shivan/optomcalc/

COPY poetry.lock pyproject.toml ${PROJECT_DIR}/

RUN poetry install

COPY . . 

