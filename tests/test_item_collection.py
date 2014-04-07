import collections

from pytest import fixture, raises

from flask.ext.navigation.item import ItemCollection


@fixture
def item_type():
    return collections.namedtuple('Item', ['endpoint'])


@fixture
def items(item_type):
    items = {'lumpy': item_type('lumpy'),
             'nutty': item_type('nutty'),
             'cuddles': item_type('cuddles')}
    return items


def test_creation(items):
    c1 = ItemCollection()
    assert repr(c1) == 'ItemCollection([])'
    assert len(c1) == 0

    c2 = ItemCollection([items['cuddles']])
    assert repr(c2) == "ItemCollection([Item(endpoint='cuddles')])"
    assert len(c2) == 1


def test_sequence(items, item_type):
    c = ItemCollection()
    raises(KeyError, lambda: c['cuddles'])
    raises(IndexError, lambda: c[0])
    assert len(c) == 0

    c.append(items['cuddles'])
    assert len(c) == 1
    assert c['cuddles'] == item_type('cuddles')
    assert c[0] == item_type('cuddles')

    c.extend([items['nutty'], items['lumpy']])
    assert len(c) == 3
    assert c['cuddles'] == item_type('cuddles')
    assert c['nutty'] == item_type('nutty')
    assert c['lumpy'] == item_type('lumpy')
    assert c[0] == item_type('cuddles')
    assert c[1] == item_type('nutty')
    assert c[2] == item_type('lumpy')

    del c[1]
    raises(KeyError, lambda: c['nutty'])
    raises(IndexError, lambda: c[2])
    assert len(c) == 2
    assert c['cuddles'] == item_type('cuddles')
    assert c['lumpy'] == item_type('lumpy')
    assert c[0] == item_type('cuddles')
    assert c[1] == item_type('lumpy')

    c.insert(0, items['nutty'])
    assert len(c) == 3
    assert c[0] == item_type('nutty')
    assert c[1] == item_type('cuddles')
    assert c[2] == item_type('lumpy')

    c[2] = item_type('happy-tree')
    assert len(c) == 3
    assert c[2] == item_type('happy-tree')
    assert c['happy-tree'] == item_type('happy-tree')
    raises(KeyError, lambda: c['lumpy'])

    with raises(TypeError):
        c['pu'] = item_type('pu')

    with raises(IndexError):
        c[3] = item_type('pu')
