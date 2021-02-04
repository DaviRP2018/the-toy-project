build:
	docker-compose build
up:
	docker-compose -p the_toy_project up
ssh:
	docker run -it blogapp /bin/bash
server:
	docker-compose exec blogapp python manage.py runserver
down:
	docker-compose -p the_toy_project down
flake8:
	docker-compose exec blogapp flake8 .
test:
	docker-compose exec blogapp python manage.py test
migrate:
	docker-compose exec blogapp python manage.py migrate
