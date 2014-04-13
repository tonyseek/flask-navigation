from flask import Flask

from .ext import nav
from .views import bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    nav.init_app(app)
    app.register_blueprint(bp)
    return app


class Config(object):
    DEBUG = True
    NEWS_SPECIAL_PAGE = 42
