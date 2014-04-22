import collections

from pytest import fixture, raises
from mock import Mock

from flask.ext.navigation.item import ItemCollection, ItemReference


class Item(collections.namedtuple('Item', ['endpoint'])):
    @property
    def ident(self):
        return self.endpoint, ()


@fixture
def items():
    items = {'lumpy': Item('lumpy'),
             'nutty': Item('nutty'),
             'cuddles': Item('cuddles')}
    return items


def test_creation(items):
    c1 = ItemCollection()
    assert repr(c1) == 'ItemCollection([])'
    assert len(c1) == 0

    c2 = ItemCollection([items['cuddles']])
    assert repr(c2) == "ItemCollection([Item(endpoint='cuddles')])"
    assert len(c2) == 1


def test_sequence(items):
    c = ItemCollection()
    raises(KeyError, lambda: c['cuddles'])
    raises(IndexError, lambda: c[0])
    assert len(c) == 0

    c.append(items['cuddles'])
    assert len(c) == 1
    assert c['cuddles'] == Item('cuddles')
    assert c[0] == Item('cuddles')

    c.extend([items['nutty'], items['lumpy']])
    assert len(c) == 3
    assert c['cuddles'] == Item('cuddles')
    assert c['nutty'] == Item('nutty')
    assert c['lumpy'] == Item('lumpy')
    assert c[0] == Item('cuddles')
    assert c[1] == Item('nutty')
    assert c[2] == Item('lumpy')

    del c[1]
    raises(KeyError, lambda: c['nutty'])
    raises(IndexError, lambda: c[2])
    assert len(c) == 2
    assert c['cuddles'] == Item('cuddles')
    assert c['lumpy'] == Item('lumpy')
    assert c[0] == Item('cuddles')
    assert c[1] == Item('lumpy')

    c.insert(0, items['nutty'])
    assert len(c) == 3
    assert c[0] == Item('nutty')
    assert c[1] == Item('cuddles')
    assert c[2] == Item('lumpy')

    c[2] = Item('happy-tree')
    assert len(c) == 3
    assert c[2] == Item('happy-tree')
    assert c['happy-tree'] == Item('happy-tree')
    raises(KeyError, lambda: c['lumpy'])

    with raises(TypeError):
        c['pu'] = Item('pu')

    with raises(IndexError):
        c[3] = Item('pu')


def test_getitem_with_args():
    item_with_args = Mock(endpoint='nutty', args={'i': 12},
                          ident=ItemReference('nutty', {'i': 12}))
    c = ItemCollection([item_with_args])

    raises(KeyError, lambda: c['nutty'])
    raises(KeyError, lambda: c['nutty', {'i': 1}])

    assert c['nutty', {'i': 12}] == item_with_args


def test_iterable(items):
    c = ItemCollection([items['cuddles'], items['lumpy']])
    iterable = iter(c)

    item = next(iterable)
    assert item.endpoint == 'cuddles'

    item = next(iterable)
    assert item.endpoint == 'lumpy'

    with raises(StopIteration):
        next(iterable)
