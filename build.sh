#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

cd portfolio
python manage.py collectstatic --noinput
python manage.py migrate
