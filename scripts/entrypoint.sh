#!/bin/bash


echo "Applying migrations..."
python manage.py migrate

echo "Collecting static"
python manage.py collectstatic --no-input

echo "Init Admin"
python manage.py init_admin

echo "Django app is ready!"

exec "$@"
