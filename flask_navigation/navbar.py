import collections

from .item import ItemCollection
from .signals import navbar_created


class NavigationBar(collections.Iterable):
    """The navigation bar object."""

    def __init__(self, name, items=None):
        self.__name__ = name
        self.items = ItemCollection(items or [])

        # sends signal
        navbar_created.send(self.__class__, bar=self)

    def __iter__(self):
        return iter(self.items)
