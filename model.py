import random
from sqlalchemy.ext.declarative import declared_attr

from core import db


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=db.func.now())

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


class Project(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True, default=lambda: random.randint(1000001, 9999999))
    contact = db.Column(db.String(50), nullable=False, default='')
    phone = db.Column(db.String(20), nullable=False, default='')
    title = db.Column(db.String(50), nullable=False, default='')
    desc = db.Column(db.TEXT, nullable=False, default='')
    file = db.Column(db.String(191), nullable=False, default='')


class UploadRecord(TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer)
    mimetype = db.Column(db.String(50))
    filename = db.Column(db.String(50))
    url = db.Column(db.String(191))
    # Content-type: application/x-zip-compressed application/zip application/gzip
    # Content-type: application/octet-stream