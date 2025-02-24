#!/bin/sh

set -e 

sleep 10
python manage.py collectstatic --no-input
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python ./user_defined/cryptoengine.py --no-input

uwsgi --socket :8000 --master --enable-threads --module secure_note.wsgi