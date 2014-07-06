from pytest import fixture, raises

from flask.ext.navigation.item import ItemCollection


class FakeItem(object):
    def __init__(self, name):
        self.__name__ = name
        self.endpoint = name

    def __repr__(self):
        return "Item(endpoint='%s')" % self.endpoint

    def __eq__(self, other):
        if not isinstance(other, FakeItem):
            return NotImplemented
        return self.__name__ == other.__name__


@fixture
def items():
    items = {'lumpy': FakeItem('lumpy'),
             'nutty': FakeItem('nutty'),
             'cuddles': FakeItem('cuddles')}
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
    assert c['cuddles'] == FakeItem('cuddles')
    assert c[0] == FakeItem('cuddles')

    c.extend([items['nutty'], items['lumpy']])
    assert len(c) == 3
    assert c['cuddles'] == FakeItem('cuddles')
    assert c['nutty'] == FakeItem('nutty')
    assert c['lumpy'] == FakeItem('lumpy')
    assert c[0] == FakeItem('cuddles')
    assert c[1] == FakeItem('nutty')
    assert c[2] == FakeItem('lumpy')

    del c[1]
    raises(KeyError, lambda: c['nutty'])
    raises(IndexError, lambda: c[2])
    assert len(c) == 2
    assert c['cuddles'] == FakeItem('cuddles')
    assert c['lumpy'] == FakeItem('lumpy')
    assert c[0] == FakeItem('cuddles')
    assert c[1] == FakeItem('lumpy')

    c.insert(0, items['nutty'])
    assert len(c) == 3
    assert c[0] == FakeItem('nutty')
    assert c[1] == FakeItem('cuddles')
    assert c[2] == FakeItem('lumpy')

    c[2] = FakeItem('happy-tree')
    assert len(c) == 3
    assert c[2] == FakeItem('happy-tree')
    assert c['happy-tree'] == FakeItem('happy-tree')
    raises(KeyError, lambda: c['lumpy'])

    with raises(TypeError):
        c['pu'] = FakeItem('pu')

    with raises(IndexError):
        c[3] = FakeItem('pu')


def test_iterable(items):
    c = ItemCollection([items['cuddles'], items['lumpy']])
    iterable = iter(c)

    item = next(iterable)
    assert item.endpoint == 'cuddles'

    item = next(iterable)
    assert item.endpoint == 'lumpy'

    with raises(StopIteration):
        next(iterable)
