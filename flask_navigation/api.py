from flask import appcontext_pushed

from .bar import NavigationBar
from .item import Item as NavigationItem


class Navigation(object):
    """The navigation extension API."""

    Bar = NavigationBar
    Item = NavigationItem

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
        self.bars = {}

    def init_app(self, app):
        appcontext_pushed.connect(self.initialize_bars, app)

    def initialize_bars(self, sender=None, **kwargs):
        """Calls the initializers of all bound navigation bars."""
        for bar in self.bars.values():
            for initializer in bar.initializers:
                initializer(self)
