web: python manage.py collectstatic --noinput; bin/gunicorn_django --workers=4 --bind=0.0.0.0:$PORT myapp/settings.py
web: gunicorn mysite.wsgi --log-file -

