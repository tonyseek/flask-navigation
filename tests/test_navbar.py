from pytest import fixture, raises

from flask.ext.navigation.navbar import NavigationBar
from flask.ext.navigation.item import Item, ItemReference


@fixture
def navbar():
    navbar = NavigationBar('mybar', [
        Item(u'Home', 'home'),
        Item(u'News', 'news'),
    ])
    return navbar


def test_attrs(navbar):
    assert navbar.name == 'mybar'
    assert len(navbar.items) == 2


def test_iterable(navbar):
    iterable = iter(navbar)

    item_1st = next(iterable)
    assert item_1st.label == u'Home'
    assert item_1st.endpoint == 'home'

    item_2nd = next(iterable)
    assert item_2nd.label == u'News'
    assert item_2nd.endpoint == 'news'

    with raises(StopIteration):
        next(iterable)

    item_reentry = next(iter(navbar))  # test for reentry iterable
    assert item_reentry.label == u'Home'
    assert item_reentry.endpoint == 'home'


def test_initializer(navbar):
    @navbar.initializer
    def initialize_more_items(nav):
        return nav
    assert navbar.initializers[0] is initialize_more_items


def test_alias_item():
    navbar = NavigationBar('mybar', [
        Item(u'Home', 'home'),
        Item(u'News', 'news', args={'page': 1}),
    ], alias={
        'foo': ItemReference('home'),
        'bar': ItemReference('news', {'page': 1}),
        'egg': ItemReference('news', {'page': 2}),
    })

    assert navbar.alias_item('foo').label == u'Home'
    assert navbar.alias_item('bar').label == u'News'

    with raises(KeyError):
        navbar.alias_item('egg')
