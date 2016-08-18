#!/bin/sh
/app/src/manage.py migrate
/app/src/manage.py runserver 0.0.0.0:8000