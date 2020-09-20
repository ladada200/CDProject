# -*- coding: utf-8 -*-

from Retrievr import app

if __name__ == '__main__':
    app.run(host=app.config['HOST_NAME'],
            port=app.config['HOST_PORT'],
            debug=app.config['DEBUG'])