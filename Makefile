PROJECTNAME=$(shell basename "$(PWD)")

MAKEFLAGS += --silent

## install: Install dependencies
install:
	pip install -r requirements.txt
## migrate: Apply DB migrations
migrate:
	python3 manage.py migrate
## run: Run production server
run:
	gunicorn core.wsgi --log-file -
## run-dev: Run developer server
run-dev:
	python manage.py runserver
## user-create: Creates a super user.
user-create:
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell
	echo "User=admin, Password=pass"

.PHONY: help
all: help
help: Makefile
	@echo
	@echo " Choose a command run in "$(PROJECTNAME)":"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo