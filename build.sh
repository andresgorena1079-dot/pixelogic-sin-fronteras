#!/bin/bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py loaddata db.json
python create_superuser.py
python manage.py migrate
python manage.py shell