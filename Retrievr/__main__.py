# -*- coding: utf-8 -*-

# from . import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)
app.config.from_object('Retrievr.config.Config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

Bootstrap(app)


from .routes import login, get_song_info

db.create_all()

app.register_blueprint(login.login_form)
app.register_blueprint(get_song_info.song)

LOG_PATH = os.path.join(os.getcwd(), "%s" % app.config.get('LOG_PATH'))

def main():
    handler = TimedRotatingFileHandler('%s/Retrievr-%s.log' % (LOG_PATH,
                                                               datetime.now().strftime("%Y-%m-%d")),
                                       when='midnight',
                                       backupCount=30)
    handler.setLevel(logging.DEBUG if app.config.get('DEBUG') else logging.INFO)
    app.logger.addHandler(handler)
    app.run(host=app.config['HOST_NAME'],
            port=app.config['HOST_PORT'],
            debug=app.config.get('DEBUG', False))

if __name__ == '__main__':
    main()