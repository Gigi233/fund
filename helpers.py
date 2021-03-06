import decimal
import re
import json
import uuid

from flask import Flask, jsonify
from datetime import date, datetime, time
from sqlalchemy.ext.declarative import declared_attr


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime):
            return o.isoformat(sep=' ', timespec='seconds')
        if isinstance(o, date):
            return o.isoformat()
        if isinstance(o, time):
            return o.isoformat(timespec='minutes')
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, uuid.UUID):
            return str(o)
        if isinstance(o, TodictModel):
            return o.todict_simple()
        else:
            return super().default(o)


class CustomFlask(Flask):
    """使用自定义的JSONEncoder，并能处理view直接返回dict"""
    json_encoder = JSONEncoder

    def make_response(self, rv):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super().make_response(rv)


class TodictModel(object):
    _todict_include = None
    _todict_exclude = None
    _todict_simple = None

    def get_field_names(self):
        # for p in self.__mapper__.iterate_properties:
        #     yield p.key
        # _keys = self.__mapper__.c.keys()
        return [x.name for x in self.__table__.columns]

    def _get_todict_keys(self, include=None, exclude=None, only=None):
        if only:
            return only

        exclude_set = {'password', 'created_at', 'updated_at'}
        if self._todict_exclude:
            exclude_set.update(self._todict_exclude)
        if exclude:
            exclude_set.update(exclude)

        include_set = set()
        if self._todict_include:
            include_set.update(self._todict_include)
        if include:
            include_set.update(include)

        keys_set = set(self.get_field_names())
        keys_set.difference_update(exclude_set)
        keys_set.update(include_set)

        return keys_set

    def todict(self, include=None, exclude=None, only=None):
        keys = self._get_todict_keys(include, exclude, only)
        data = {key: getattr(self, key) for key in keys}
        return data or None

    def todict_simple(self):
        only = self._todict_simple or [x for x in self._get_todict_keys()
                                       if x in ['id', 'name']]
        return self.todict(only=only)


class ModelMixin(TodictModel):
    @declared_attr
    def __tablename__(cls):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()