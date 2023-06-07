#!/bin/sh

echo "Starting makemigrations"
python3 manage.py flush --no-input
python3 manage.py makemigrations
python3 manage.py collectstatic --no-input
echo "Finished makemigrations"

echo "Starting migrate"
python3 manage.py migrate
echo "Finished migrate"

gunicorn app.wsgi:application --bind 0.0.0.0:9000 & # added line for launching the web app using gunicorn

exec "$@"