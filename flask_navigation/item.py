import collections

from flask import request

from .utils import LazyProperty


class Item(object):
    """The navigation item object.

    :param label: the display label of this navigation item.
    :param url: the target url of this navigation item, could be string or
                callable object which return string.
    :param kwargs: the extra data for representation. you can access it from
                   the instance's attribute ``item.extra_data``
    """

    label = LazyProperty('label', cache=True)
    url = LazyProperty('url', cache=True)

    def __init__(self, name, label, url, **kwargs):
        self.__name__ = name
        self.label = label
        self.url = url
        self.extra_data = kwargs

    @property
    def name(self):
        """The alias for ``__name__``."""
        return self.__name__

    @property
    def is_active(self):
        """``True`` if the item should be presented as active, and ``False``
        always if the request context is not bound.
        """
        return bool(request and self.is_current)

    @property
    def is_internal(self):
        """``True`` if the target url is internal of current app."""
        return self.url.is_internal

    @property
    def is_current(self):
        """``True`` if current request has same endpoint with the item.

        The property should be used in a bound request context, or the
        :class:`RuntimeError` may be raised.
        """
        if not self.is_internal:
            return False  # always false for external url
        has_same_endpoint = (request.endpoint == self.endpoint)
        has_same_args = (request.view_args == self.args)
        return has_same_endpoint and has_same_args  # matches the endpoint


class ItemCollection(collections.MutableSequence,
                     collections.Iterable):
    """The collection of navigation items.

    This collection is a mutable sequence. All items have order index, and
    could be found by its endpoint name. e.g.::

        c = ItemCollection()
        c.append(Item(endpoint='doge'))

        print(c['doge'])  # output: Item(endpoint='doge')
        print(c[0])       # output: Item(endpoint='doge')
        print(c)          # output: ItemCollection([Item(endpoint='doge')])
        print(len(c))     # output: 1

        c.append(Item(endpoint='lumpy', args={'num': 4}))

        print(c[1])       # output: Item(endpoint='lumpy', args={'num': 4})
        assert c['lumpy', {'num': 4}] is c[1]
    """

    def __init__(self, iterable=None):
        #: the item collection
        self._items = []
        #: the mapping collection of endpoint -> item
        self._items_mapping = {}
        #: initial extending
        self.extend(iterable or [])

    def __repr__(self):
        return 'ItemCollection(%r)' % self._items

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._items[index]
        else:
            return self._items_mapping[index]  # gets by name

    def __setitem__(self, index, item):
        # remove the old reference
        old_item = self._items[index]
        del self._items_mapping[old_item.__name__]

        self._items[index] = item
        self._items_mapping[item.__name__] = item

    def __delitem__(self, index):
        item = self[index]
        del self._items[index]
        del self._items_mapping[item.__name__]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def insert(self, index, item):
        self._items.insert(index, item)
        self._items_mapping[item.__name__] = item
