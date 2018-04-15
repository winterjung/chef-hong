import pathlib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from config import config

basedir = pathlib.Path(__file__).cwd()
db = SQLAlchemy()
sentry = Sentry()


def create_app(config_name):
    app = Flask(__name__)
    configuration = config[config_name]
    app.config.from_object(configuration)

    configuration.init_app(app)
    db.init_app(app)
    if issubclass(configuration, config['production']):
        sentry.init_app(app, dsn=configuration.SENTRY_DSN)

    from app.api import api as api_blueprint
    from app.util import util as util_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(util_blueprint, url_prefix='/util')

    return app
