pep8:
	@flake8 * --ignore=F403,F401 --exclude=requirements.txt,*.pyc,*.md,Dockerfile,docker-compose.yml,Makefile,LICENSE,*.in,*.conf,gunicorn_start,migrations*

clean:
	@find . -name "*.pyc" -delete

deps:
	@pip install -r requirements.txt

test: deps clean pep8
	@python manage.py test

settings:
	cp sofia/local_settings.py.example sofia/local_settings.py

docker-settings:
	cp sofia/local_settings.py.docker sofia/local_settings.py

run:
	@python manage.py runserver 8000

setup: settings deps clean
	@python manage.py syncdb
	@python manage.py migrate

help:
	grep '^[^#[:space:]].*:' Makefile | awk -F ":" '{print $$1}'
