import collections

from .item import ItemCollection
from .signals import navbar_created


class NavigationBar(collections.Iterable):
    """The navigation bar object."""

    def __init__(self, name, items=None, alias=None):
        self.__name__ = name
        self.items = ItemCollection(items or [])
        self.alias = alias or {}

        # sends signal
        navbar_created.send(self.__class__, bar=self)

    def __iter__(self):
        return iter(self.items)

    def alias_item(self, alias):
        """Gets an item by its alias."""
        ident = self.alias[alias]
        return self.items[ident]
