import os
from models import db
from flask import Flask
from flasgger import Swagger
from views import weather
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_app():
    ''' Helper for creating the Flask app.'''
    flask_app = Flask(__name__)
    flask_app.config['DEBUG'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    db.init_app(flask_app)
    flask_app.register_blueprint(weather, url_prefix='')
    Swagger(flask_app)
    return flask_app


def setup_database(flask_app):
    ''' Helper for setting up the database.'''
    with flask_app.app_context():
        logger.debug('Creating database...')
        db.create_all()


if __name__ == '__main__':
    app = create_app()
    # Because this is just a demonstration we set up the database like this.
    if not os.path.exists('instance/database.db'):
        logger.debug('Database not found, creating...')
        setup_database(app)

    app.run(debug=True, port=8000)
