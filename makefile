run:
	@echo "Running application"
	cd app && \
	pipenv run python manage.py runserver

run-prod:
	@echo "Running applicaition in docker container"
	cd app && \
	docker-compose up -d --build

migrate: 
	cd app && \
	pipenv run python manage.py collectstatic --no-input && \
	pipenv run python manage.py makemigrations --no-input && \
	pipenv run python manage.py migrate --no-input

.PHONY: test
test:
	@echo "Running automated testing"
	cd app && \
	pipenv run pytest -vv

deploy:
	@echo "Deploying to remote server"
	cp app/.env ansible/templates/.env
	pipenv run ansible-playbook ansible/deploy.yml -i ansible.hosts -K
