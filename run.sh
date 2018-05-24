#!/usr/bin/env bash
FLASK_APP=app.py flask run -h 127.0.0.1 -p 7040
#gunicorn -w 2 -b 127.0.0.1:7040 app:app