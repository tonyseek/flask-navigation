import collections


class ItemCollection(collections.MutableSequence):
    """The collection of navigation items.

    This collection is a mutable sequence. All items have order index, and
    could be found by its endpoint name. e.g.::

    >>> item_type = collections.namedtuple('Item', ['endpoint'])
    >>>
    >>> c = ItemCollection()
    >>> c.append(item_type(endpoint='doge'))
    >>>
    >>> c['doge']
    Item(endpoint='doge')
    >>> c[0]
    Item(endpoint='doge')
    >>> c
    ItemCollection([Item(endpoint='doge')])
    >>> len(c)
    1
    """

    def __init__(self, iterable=[]):
        #: the item collection
        self._items = []
        #: the mapping collection of endpoint -> item
        self._items_mapping = {}
        #: initial extending
        self.extend(iterable)

    def __repr__(self):
        return 'ItemCollection(%r)' % self._items

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._items[index]
        else:
            return self._items_mapping[index]

    def __setitem__(self, index, item):
        # remove the old reference
        old_item = self._items[index]
        del self._items_mapping[old_item.endpoint]

        self._items[index] = item
        self._items_mapping[item.endpoint] = item

    def __delitem__(self, index):
        endpoint = self[index].endpoint
        del self._items[index]
        del self._items_mapping[endpoint]

    def __len__(self):
        return len(self._items)

    def insert(self, index, item):
        self._items.insert(index, item)
        self._items_mapping[item.endpoint] = item
