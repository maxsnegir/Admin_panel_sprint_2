#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Загрузка данных из sqlite"
cd sqlite_to_postgres
python load_data.py
echo "Загрузка завершена"

cd ../movies_admin

python manage.py migrate movies --fake
python manage.py migrate

python manage.py collectstatic --no-input

# Решил тут оставить, насколько понимаю в Dockerfile нельзя и entrypoint запустить и CMD
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000