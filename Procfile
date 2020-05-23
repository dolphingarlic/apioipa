web: gunicorn apioipa.wsgi --log-file -
release: python manage.py migrate; sh load_problems.sh