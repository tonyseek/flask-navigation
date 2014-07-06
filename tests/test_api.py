from pytest import fixture

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
