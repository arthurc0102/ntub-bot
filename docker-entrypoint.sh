#!/bin/sh
set -e

echo "Waiting for Database to start...."
sleep 5

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Migrating Database"
python3 manage.py migrate

exec "$@"
