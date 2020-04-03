web: gunicorn apioipa.wsgi --log-file -
release: python manage.py migrate; python manage.py loaddata problems