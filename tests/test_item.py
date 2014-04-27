from pytest import fixture, raises
from flask import Markup

from flask.ext.navigation.item import Item, ItemReference


@fixture
def items():
    items = {'biu': Item(u'Biu', endpoint='biu.biu'),
             'boom1': Item(u'Boom', endpoint='biu.boom', args={'num': 1}),
             'boom2': Item(u'Boom', endpoint='biu.boom',
                           args=lambda: {'num': 2}),
             'example': Item(u'Example', endpoint='external.example',
                             url='//example.com')}
    return items


def test_basic(app, items):
    # without args
    assert items['biu'].label == u'Biu'
    assert items['biu'].args == {}
    assert items['biu'].url == 'http://example.dev/biu/biu'

    # with static args
    assert items['boom1'].label == u'Boom'
    assert items['boom1'].args == {'num': 1}
    assert items['boom1'].url == 'http://example.dev/biu/boom/1'

    # with dynamic args
    assert items['boom2'].label == u'Boom'  # non-conflic label
    assert items['boom2'].args == {'num': 2}
    assert items['boom2'].url == 'http://example.dev/biu/boom/2'

    # hard-coding url
    assert items['example'].label == u'Example'
    assert items['example'].args == {}
    assert items['example'].url == '//example.com'


def test_is_active(app, items):
    with app.test_client() as client:
        client.get('/biu/boom/2')
        assert not items['biu'].is_active
        assert not items['boom1'].is_active
        assert items['boom2'].is_active
        assert not items['example'].is_active

    with app.test_client() as client:
        client.get('/biu/boom/1')
        assert not items['biu'].is_active
        assert items['boom1'].is_active
        assert not items['boom2'].is_active
        assert not items['example'].is_active

    with app.test_client() as client:
        client.get('/biu/biu')
        assert items['biu'].is_active
        assert not items['boom1'].is_active
        assert not items['boom2'].is_active
        assert not items['example'].is_active


def test_ident(items):
    assert items['biu'].endpoint != items['boom1'].endpoint
    assert items['boom1'].endpoint == items['boom2'].endpoint

    assert items['biu'].ident != items['boom1'].ident
    assert items['boom1'].ident != items['boom2'].ident


def test_item_reference():
    assert ItemReference('foo').endpoint == 'foo'
    assert ItemReference('foo').args == ()
    assert ItemReference('foo') == ItemReference('foo', {})

    assert ItemReference('bar', {'a': 1}).endpoint == 'bar'
    assert ItemReference('bar', {'b': 2, 'a': 1}).args == (('a', 1), ('b', 2))


def test_html_representation(app, items):
    with app.test_client() as client:
        client.get('/biu/biu')

        # without format_spec
        assert str(Markup(items['biu'])) == \
            '<a class="active" href="/biu/biu">Biu</a>'
        assert str(Markup(items['boom1'])) == \
            '<a href="/biu/boom/1">Boom</a>'

        # "li" as format_spec
        assert str(Markup('{0:li}').format(items['biu'])) == \
            '<li class="active"><a class="active" href="/biu/biu">Biu</a></li>'
        assert str(Markup('{0:li}').format(items['boom1'])) == \
            '<li><a href="/biu/boom/1">Boom</a></li>'

        # default format_spec
        assert str(Markup('{0:}').format(items['biu'])) == \
            '<a class="active" href="/biu/biu">Biu</a>'
        assert str(Markup('{0:}').format(items['boom1'])) == \
            '<a href="/biu/boom/1">Boom</a>'

        # invalid format_spec
        with raises(ValueError):
            str(Markup('{0:foo}').format(items['biu']))


def test_html_representation_with_class(app):
    biu_with_class = Item(
        u'Biu', endpoint='biu.biu',
        html_attrs={'class': ['icon', 'icon-biu'], 'data-icon': 'biu'})
    boom_with_class = Item(
        u'Boom', endpoint='biu.boom', args={'num': 1},
        html_attrs={'class': ['icon', 'icon-boom'], 'data-icon': 'boom'})

    with app.test_client() as client:
        client.get('/biu/biu')

        assert str(Markup(biu_with_class)) == (
            '<a class="icon icon-biu active" data-icon="biu"'
            ' href="/biu/biu">Biu</a>')
        assert str(Markup(boom_with_class)) == (
            '<a class="icon icon-boom" data-icon="boom"'
            ' href="/biu/boom/1">Boom</a>')
