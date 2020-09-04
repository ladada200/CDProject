    # -*- coding: utf-8 -*-

import logging
import psycopg2

_logger = logging.getLogger(__name__)

class DBConnection:
    """Database connection params for Postgresql"""

    _dbname = None
    _dbhost = "localhost"
    _dbport = 5432
    _dbuser = "dbadmin"
    _dbpass = "dbpass"
    _dbtable = None

    def __init__(self,
                dbname=None,
                dbport=None,
                dbhost=None,
                dbuser=None,
                dbpass=None):
        """Initializes thes class"""

        params = [dbname, dbport, dbhost, dbuser, dbpass]

        try:
            for each in params:
                if not each:
                    raise Exception("Unable to complete connection, missing required parameter")
            
            self._dbname = dbname
            self._dbhost = dbhost
            self._dbport = dbport
            self._dbuser = dbuser
            self._dbpass = dbpass

        except Exception as e:
            _logger.debug("[ DB Connection ] > {error}".format(error=e))
        finally:
            return 0

    def setTable(self, table=None):
        """Changing table names"""
        if table:
            self._dbtable = table

    def connect(self):
        """Used for connecting to DB"""
        return psycopg2.connect(user=self._dbuser,
                                password=self._dbpass,
                                host=self._dbhost,
                                port=self._dbport,
                                database=self._dbname).cursor()

    if __name__ == __main__:
        return 0