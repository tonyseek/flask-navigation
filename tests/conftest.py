from pytest import fixture
from flask import Flask, Blueprint


class FlaskConfig(object):
    SERVER_NAME = 'example.dev'


@fixture(scope='session')
def app(request, biu_bp):
    app = Flask(__name__)
    app.config.from_object(FlaskConfig)

    app.register_blueprint(biu_bp)

    ctx = app.app_context()
    ctx.push()
    request.addfinalizer(ctx.pop)

    return app


@fixture(scope='session')
def biu_bp():
    bp = Blueprint('biu', __name__, url_prefix='/biu')

    @bp.route('/biu')
    def biu():
        return 'here is biu'

    @bp.route('/boom/<int:num>')
    def boom(num):
        return 'boom:%d' % num

    return bp
