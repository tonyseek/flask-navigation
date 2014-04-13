from flask.signals import Namespace


signals = Namespace()


navbar_created = signals.signal('navbar-created')
