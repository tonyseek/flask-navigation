from pytest import fixture

from flask.ext.navigation.item import Item


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
