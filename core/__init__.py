from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.local import LocalProxy
from helpers import ModelMixin
from .flask_oss import FlaskOSS

db = SQLAlchemy(model_class=ModelMixin)
oss = FlaskOSS()
logger = LocalProxy(lambda: current_app.logger)
