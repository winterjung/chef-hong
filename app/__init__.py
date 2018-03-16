import pathlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

basedir = pathlib.Path(__file__).cwd()

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    config[config_name].init_app(app)

    db.init_app(app)

    from app.api import api as api_blueprint
    from app.util import util as util_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(util_blueprint, url_prefix='/util')

    return app
