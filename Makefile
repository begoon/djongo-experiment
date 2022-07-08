all:

PYTHON := python3

MANAGE := $(PYTHON) manage.py

manage:
	$(MANAGE) $(cmd)

migrate:
	$(MANAGE) migrate

migrations:
	$(MANAGE) makemigrations

test: flake black unittest

web:
	gunicorn application.wsgi \
		--reload \
		--bind 0.0.0.0:8000

include Makefile.colors
include Makefile.dev
include Makefile.docker
include Makefile.pip
include Makefile.unittest