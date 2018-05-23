from flask import request
from wtforms import Form
from wtforms import StringField, Field
from wtforms.validators import DataRequired, Length, URL, Regexp
from model import Project
from core import db

PHONE_REGEX = '^1[3-9]\d{9}$'


class PhoneNumber(Regexp):
    def __init__(self):
        super().__init__(PHONE_REGEX, message='手机号格式错误')


class JSONForm(Form):
    class Meta:
        locales = ['en']

    def __init__(self, item=None, data=None):
        if data is None:
            data = request.get_json()
        super().__init__(data=data)


class UploadProjectForm(JSONForm):
    contact = Field('contact', [DataRequired(), Length(max=50, min=1)])
    phone = StringField('phone', [DataRequired()], PhoneNumber())
    title = StringField('title', [DataRequired(), Length(max=50, min=1)])
    desc = StringField('desc', [DataRequired(), Length(min=1)])
    file = StringField('file', [DataRequired(), URL()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self):
        item = Project()
        item.contact = self.name.contact
        item.phone = self.phone.data
        item.title = self.title.data
        item.desc = self.desc.data
        item.file = self.file.data
        db.session.add(item)
        db.session.commit()
        return item
