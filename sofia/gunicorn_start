#!/bin/bash

NAME="{{ project_name }}"
DJANGODIR=/webapps/{{ project_name }}/{{ project_name }}
SOCKFILE=/webapps/{{ project_name }}/run/gunicorn.sock
USER=webapps
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE={{ project_name }}.settings
DJANGO_WSGI_MODULE={{ project_name }}.wsgi

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER \
  --log-level=debug \
  --bind=unix:$SOCKFILE