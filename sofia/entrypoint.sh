make setup
make docker-settings
python /sofia/manage.py syncdb
python /sofia/manage.py migrate
python /sofia/manage.py runserver 0.0.0.0:8000
