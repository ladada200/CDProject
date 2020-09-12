# -*- coding: utf-8 -*-

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

    _table = None
    _log_access = True

    def __init__(self):
        self._table = self.__tablename__.replace('.', '_')
        return super(BaseMixin, self)


    @classmethod
    def create(self, vals):
        try:
            if self._log_access:
                vals['create_date'] = datetime.now()
                vals['write_date'] = datetime.now()
    
            obj = self(vals)
            db.session.add(obj)
            db.session.commit()
            app.logger.debug("%s [CREATE]: %s" % (self.__tablename__, vals))
        except Exception as e:
            db.session.rollback()

    @classmethod
    def write(self, vals, uuid=None):
        try:
            if not self:
                return True

            if self._log_access:
                if 'write_date' not in vals.keys():
                    vals['write_date'] = datetime.now()

            query = 'UPDATE "%s" SET %s WHERE uuid = \'%s\';' % (
                self.__tablename__, ','.join('\"%s\"=\'%s\'' % (e, vals[e]) for e in vals.keys()), uuid
            )

            db.engine.execute(query)
            db.session.commit()
            app.logger.debug("%s [WRITE]: %s" % (self.__tablename__, vals))
            return True
        except Exception as e:
            db.session.rollback()