# -*- coding: utf-8 -*-

# from . import db
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from cryptography.fernet import Fernet

import logging
import os
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler

def _fkey():
    return Fernet(b"%s" % app.config.get('FERNET_KEY').encode())

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=30)
app.config.from_object('Retrievr.config.Config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

Bootstrap(app)


from .routes import login, get_song_info


app.register_blueprint(login.login_form)
app.register_blueprint(get_song_info.song)

LOG_PATH = os.path.join(os.getcwd(), "%s" % app.config.get('LOG_PATH'))

def main():
    db = SQLAlchemy(app)
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    werk_log = logging.getLogger('werkzeug')
    handler = TimedRotatingFileHandler('%s/Retrievr-%s.log' % (LOG_PATH,
                                                               datetime.now().strftime("%Y-%m-%d")),
                                       when='midnight',
                                       backupCount=30)
    handler.setLevel(logging.DEBUG if app.config.get('DEBUG') else logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    app.logger.setLevel(logging.DEBUG if app.config.get('DEBUG') else logging.INFO)
    app.logger.addHandler(handler)
    werk_log.addHandler(handler)

    db.create_all()

    superuser = db.session.execute('SELECT EXISTS (SELECT * FROM private.auth_users WHERE login like \'%s\') AS SUPERUSERID;' % app.config.get('ADMIN_USER').replace('"', ""))
    superuser = [dict(row) for row in superuser][0]
    if not superuser.get('superuserid'):
        app.logger.debug("Missing default Administrator; creating.")
        db.session.execute("INSERT INTO private.auth_users (login, password, email, active, accepted_invite) VALUES (\'{login}\', \'{password}\', \'{email}\', true, true)".format(
            login=app.config.get('ADMIN_USER').replace('"', ""),
            password=_fkey().encrypt(app.config.get('ADMIN_PASS').replace('"', "").encode()).decode(),
            email=app.config.get('ADMIN_USER').replace('"', "")
        ))
    db.session.commit()
    db.session.close()

    app.run(host=app.config['HOST_NAME'],
            port=app.config['HOST_PORT'],
            debug=app.config.get('DEBUG', False))

if __name__ == '__main__':
    main()