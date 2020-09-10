# -*- coding: utf-8 -*-

from Retrievr import Retrievr

# app.register_blueprint(Retrievr.routes)

# db = SQLAlchemy(app)

if __name__ == '__main__':
    Retrievr.run(host=Retrievr.config['HOST_NAME'], port=Retrievr.config['HOST_PORT'], debug=Retrievr.config['DEBUG'])