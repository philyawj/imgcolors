# Install

virtualenv imgcolorsenv

django-admin startproject imgcolors

source imgcolorsenv/bin/activate
pip install django==2.2.\*
pip install psycopg2-binary

cd into django folder
python manage.py migrate
python manage.py runserver

python manage.py startapp colors

pip install Pillow
