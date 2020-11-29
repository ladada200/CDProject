# -*- coding: utf-8 -*-

from flask import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime
from cryptography.fernet import Fernet
from . import app

db = SQLAlchemy()

def _fkey():
    return Fernet(b"%s" % app.config.get('FERNET_KEY').encode())

LOG_ACCESS_COLUMNS = ['create_uid', 'create_date', 'write_uid', 'write_date']

class Encryption(object):
    def encrypt(self, data=None):
        if data:
            data = _fkey().encrypt(data.encode())
        return data.decode()

    def decrypt(self, data=None):
        if data:
            data = _fkey().decrypt(data.encode())
        return data.decode()

class BaseMixin(object):

    _cr = property(lambda self: self.env.cr)

    _table = None
    _log_access = True

    def __init__(self):
        return None

    @classmethod
    def create(self, vals):
        try:   
            if not self:
                return True

            self._table = ".".join([self.__table_args__.get('schema'), self.__tablename__])

            __dict__ = self.__dict__

            if session and self._log_access:
                vals['create_uid'] = session.get('context').get('uid')
                vals['write_uid'] = session.get('context').get('uid')

            obj = self(vals)
            db.session.add(obj)
            db.session.commit()
            app.logger.debug("%s [CREATE]: %s" % (self._table, vals))
            return super(BaseMixin, self).create(vals)
        except Exception as e:
            app.logger.error("%s" % e)
            db.session.rollback()

    @classmethod
    def write(self, vals, uuid=None):
        try:
            if not self:
                return True

            self._table = ".".join([self.__table_args__.get('schema'), self.__tablename__])

            __dict__ = self.__dict__

            if session and self._log_access:
                vals['write_uid'] = session.get('context').get('uid')

            query = 'UPDATE %s SET %s WHERE uuid=\'%s\';' % (
                self._table, ','.join('\"%s\"=\'%s\'' % (e, vals[e]) for e in vals.keys()), uuid
            )

            db.engine.execute(query)
            db.session.commit()
            app.logger.debug("%s [WRITE]: %s" % (self._table, vals))
            return True
        except Exception as e:
            app.logger.error("%s" % e)
            db.session.rollback()

    @classmethod
    def unlink(self):
        """Default unlink method"""
        try:
            if not self:
                return True

            self._table = ".".join([self.__table_args__.get('schema'), self.__tablename__])

            __dict__ = self.__dict__

            if session and self._log_access:
                vals['write_uid'] = session.get('context').get('uid')

            query = """DELETE FROM {schema}.{tablename} WHERE {input}"""

            query.format(schema=self.__table_args__.get('schema'),
                         tablename=self.__tablename__,
                         input="id=%s" % self.id)

            db.engine.execute(query)
            db.session.commit()
            app.logger.debug("%s [UNLINK]: %s" % (self._table, ))
        except Exception as e:
            app.logger.error("%s" % e)
            db.session.rollback()