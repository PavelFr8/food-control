#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "Postgres is up"

python manage.py migrate --noinput

python manage.py loaddata fixtures/roles.json

python manage.py loaddata fixtures/menu.json

python manage.py loaddata fixtures/users.json

python manage.py loaddata fixtures/payments.json

python manage.py loaddata fixtures/meals.json

exec gunicorn food_control.wsgi:application --bind 0.0.0.0:8000 --workers 3 --capture-output --log-level debug
