#!/bin/sh
set -e

poetry run python3 /app/src/manage.py migrate --noinput

exec "$@"
