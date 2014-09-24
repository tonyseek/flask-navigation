from pytest import fixture

from flask import Flask, current_app
from flask.ext.navigation.api import Navigation
from flask.ext.navigation.navbar import NavigationBar
from flask.ext.navigation.item import Item


@fixture
def nav(app):
    nav = Navigation(app)
    nav.Bar('top', [
        nav.Item('Biu', endpoint='biu.biu'),
        nav.Item('Boom', endpoint='biu.boom', args={'num': 1}),
    ])
    return nav


def test_bound_bar(app, nav):
    # ensure the navbar has been bound
    top = nav['top']

    assert nav.Bar.__bases__ == (NavigationBar,)
    assert isinstance(top, nav.Bar)

    assert nav.Item.__bases__ == (Item,)
    assert isinstance(top.items['biu.biu'], nav.Item)


def test_initializer():
    app = Flask(__name__)
    app.config.setdefault('BIU_NUM', 42)

    nav = Navigation()
    nav.init_app(app)

    woo = nav.Bar('woo')

    @woo.initializer
    def initialize_woo(nav):
        boom_num = current_app.config['BIU_NUM']
        nav['woo'].items.extend([
            nav.Item('Boom', endpoint='biu', args={'num': boom_num}),
        ])

    @app.route('/')
    def index():
        return woo.items[0].url

    @app.route('/biu/<int:num>')
    def biu():
        return ''

    with app.test_client() as c:
        url = c.get('/')
        assert url.data == b'/biu/42'


def test_current_item():
    app = Flask(__name__)

    nav = Navigation()
    nav.init_app(app)
    news_item = Item(u'News', 'news')
    navbar = nav.Bar('test_current', [
        Item(u'Home', 'home'),
        news_item,
    ])

    @app.route('/')
    def home():
        pass

    @app.route('/news')
    def news():
        pass

    assert navbar.current_item is None

    with app.test_request_context('/news'):
        assert navbar.current_item == news_item


def test_current_item_nested():
    app = Flask(__name__)

    nav = Navigation()
    nav.init_app(app)
    item = Item('Nested item', 'nested')
    navbar = nav.Bar('test_current', [
        Item(u'Home', 'home'),
        Item(u'News', 'news'),
        Item(u'With Children', 'with_children', items=[item])
    ])

    @app.route('/')
    def home():
        pass

    @app.route('/nested')
    def nested():
        pass

    assert navbar.current_item is None

    with app.test_request_context('/nested'):
        assert navbar.current_item == item
