release: python manage.py migrate
web: gunicorn djangoconverter.wsgi --log-file=-
worker: celery worker --app=tasks.djangoconverter