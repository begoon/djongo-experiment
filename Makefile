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
	gunicorn ingress.wsgi \
		--reload \
		--bind 127.0.0.1:10000

include Makefile.colors
include Makefile.dev
include Makefile.pip
include Makefile.unittest
