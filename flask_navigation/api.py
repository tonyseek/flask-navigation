from flask.signals import appcontext_pushed

from .navbar import NavigationBar
from .item import Item, ItemReference
from .utils import BoundTypeProperty
from .signals import navbar_created


class Navigation(object):
    """The navigation extension API."""

    Bar = BoundTypeProperty('Bar', NavigationBar)
    Item = BoundTypeProperty('Item', Item)
    ItemReference = ItemReference

    def __init__(self, app=None):
        self.bars = {}
        if app is not None:
            self.init_app(app)
        # connects ext-level signals
        navbar_created.connect(self.bind_bar, self.Bar)

    def __getitem__(self, name):
        """Gets a bound navigation bar by its name."""
        return self.bars[name]

    def init_app(self, app):
        # connects app-level signals
        appcontext_pushed.connect(self.initialize_bars, app)
        # integrate with jinja template
        app.jinja_env.globals['nav'] = self

    def initialize_bars(self, sender=None, **kwargs):
        """Calls the initializers of all bound navigation bars."""
        for bar in self.bars.values():
            for initializer in bar.initializers:
                initializer(self)

    def bind_bar(self, sender=None, **kwargs):
        """Binds a navigation bar into this extension instance."""
        bar = kwargs.pop('bar')
        self.bars[bar.name] = bar
