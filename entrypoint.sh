#!/bin/bash

postgres_ready() {
python << END
import sys
import psycopg2
try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${DB_HOST}",
        port="${DB_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

echo "Загрузка данных из sqlite"
# Если не запускать файл напрямую, то файл sqlite создается в каталоге sqlite_to_postgres
# и из-за этого падает, решил "накостылить" c переходом в папку
cd sqlite_to_postgres
python load_data.py
echo "Загрузка завершена"

cd ../movies_admin
python manage.py migrate --no-input
python manage.py makemigrations --no-input
python manage.py migrate --fake --no-input
python manage.py collectstatic --no-input

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000