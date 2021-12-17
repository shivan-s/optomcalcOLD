run:
	@echo "Running application"
	pipenv run python app/manage.py runserver

run-prod:
	@echo "Running applicaition in docker container"
	docker-compose up -d --build

migrate:
	pipenv run python app/manage.py collectstatic --no-input && \
	pipenv run python app/manage.py makemigrations --no-input && \
	pipenv run python app/manage.py migrate --no-input

.PHONY: test
test:
	@echo "Running automated testing"
	pipenv run pytest -vv app/

deploy:
	@echo "Deploying to remote server"
	cp .env ansible/files/.env
	pipenv run ansible-playbook ansible/deploy.yml -i ansible/hosts -K
