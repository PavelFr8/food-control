#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "Postgres is up"

python manage.py migrate --noinput

exec gunicorn food_control.wsgi:application --bind 0.0.0.0:8000 --workers 3
