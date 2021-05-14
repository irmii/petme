#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

#echo "Load test fixtures"
#python manage.py loadtestfixtures tests

exec "$@"
