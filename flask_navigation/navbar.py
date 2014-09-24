import collections

from .item import ItemCollection
from .signals import navbar_created


class NavigationBar(collections.Iterable):
    """The navigation bar object."""

    def __init__(self, name, items=None, alias=None):
        self.name = name
        self.items = ItemCollection(items or [])
        self.initializers = []
        self.alias = alias or {}

        # sends signal
        navbar_created.send(self.__class__, bar=self)

    def __iter__(self):
        return iter(self.items)

    def initializer(self, fn):
        """Adds a initializer function.

        If you want to initialize the navigation bar within a Flask app
        context, you can use this decorator.

        The decorated function should nave one paramater ``nav`` which is the
        bound navigation extension instance.
        """
        self.initializers.append(fn)
        return fn

    def alias_item(self, alias):
        """Gets an item by its alias."""
        ident = self.alias[alias]
        return self.items[ident]

    @property
    def current_item(self):
        """Get the current active navigation Item if any.

        .. versionadded:: 0.2.0
        """
        return self._get_current_item(self)

    def _get_current_item(self, items):
        for item in items:
            if item.is_active:
                return item
            else:
                nested = self._get_current_item(item.items)
                if nested:
                    return nested
