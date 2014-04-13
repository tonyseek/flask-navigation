import collections

from .item import ItemCollection
from .signals import navbar_created


class NavigationBar(collections.Iterable):
    """The navigation bar object."""

    def __init__(self, name, items=[], parent_navbar=None,
                 parent_endpoint=None):
        self.name = name
        self.items = ItemCollection(items)
        self.initializers = []

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
