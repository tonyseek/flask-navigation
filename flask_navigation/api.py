from flask.signals import appcontext_pushed

from .navbar import NavigationBar
from .item import Item, ItemReference
from .utils import BoundTypeProperty
from .signals import navbar_created


class Navigation(object):
    """The navigation extension API."""

    #: The subclass of :class:`~flask.ext.navigation.navbar.NavigationBar`. It
    #: bound with the the current instance.
    #:
    #: :type: :class:`~flask.ext.navigation.utils.BoundTypeProperty`
    Bar = BoundTypeProperty('Bar', NavigationBar)

    #: The subclass of :class:`~flask.ext.navigation.item.Item`. It bound with
    #: the the current instance.
    #:
    #: :type: :class:`~flask.ext.navigation.utils.BoundTypeProperty`
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
        """Initializes an app to work with this extension.

        The app-context signals will be subscribed and the template context
        will be initialized.

        :param app: the :class:`flask.Flask` app instance.
        """
        # connects app-level signals
        appcontext_pushed.connect(self.initialize_bars, app)
        # integrate with jinja template
        app.add_template_global(self, 'nav')

    def initialize_bars(self, sender=None, **kwargs):
        """Calls the initializers of all bound navigation bars."""
        for bar in self.bars.values():
            for initializer in bar.initializers:
                initializer(self)

    def bind_bar(self, sender=None, **kwargs):
        """Binds a navigation bar into this extension instance."""
        bar = kwargs.pop('bar')
        self.bars[bar.name] = bar
