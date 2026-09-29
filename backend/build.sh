#!/usr/bin/env bash
# Render / Railway build step
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py seed_demo
