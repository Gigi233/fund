#!/usr/bin/env bash
#FLASK_APP=app.py flask run
gunicorn -w 2 -b 127.0.0.1:7040 app:app