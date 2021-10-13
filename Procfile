release: python manage.py migrate --noinput
web: gunicorn --bind :$PORT

worker: celery -A petme worker -l info
beat: celery -A petme beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
