# -*- coding: utf-8 -*-

# from . import db
from flask import Flask, session, render_template, make_response
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


from .routes.main import main
from .routes.get_song_info import song
from .routes.login import login_form

app.register_blueprint(main)
app.register_blueprint(login_form, url_prefix='/web')
app.register_blueprint(song, url_prefix='/song')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    print(app.url_map)
    return make_response(render_template('/errors/error.html'), 404)

LOG_PATH = os.path.join(os.getcwd(), "%s" % app.config.get('LOG_PATH'))

def main():
    db = SQLAlchemy(app)
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    werk_log = logging.getLogger('werkzeug')
    handler = TimedRotatingFileHandler('%s/Retrievr.log' % (LOG_PATH),
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
            debug=app.config.get('DEBUG', False), use_reloader=True)

if __name__ == '__main__':
    main()