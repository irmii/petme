release: python manage.py migrate --noinput

web: gunicorn -w 1 --access-logfile=- --timeout=120 petme.wsgi:application --bind 0.0.0.0:$PORT

worker: celery -A petme worker -l info
beat: celery -A petme beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
