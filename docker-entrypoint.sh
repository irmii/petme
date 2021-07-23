#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

#echo "Load test fixtures"
#python manage.py loadtestfixtures tests

python manage.py createdefaultsuperuser

exec "$@"
