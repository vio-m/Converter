release: python manage.py migrate
web: gunicorn djangoconverter.wsgi --log-file=-
worker: celery -A djangoconverter worker -P threads -E