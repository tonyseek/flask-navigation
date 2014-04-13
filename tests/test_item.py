from pytest import fixture

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
