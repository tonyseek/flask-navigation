Flask-Navigation
================

Installation
------------

::

    $ pip install Flask-Navigation

Set Up
------

Just like the most of Flask extension::

    from flask import Flask
    from flask.ext.navigation import Navigation

    app = Flask(__name__)
    nav = Navigation(app)

Or use the app factory pattern::

    nav = Navigation()
    nav.init_app(app)

API
---

Extension Class
~~~~~~~~~~~~~~~

.. autoclass:: flask.ext.navigation.Navigation
   :members: init_app, Bar, Item, ItemReference

Internal Classes
~~~~~~~~~~~~~~~~

.. autoclass:: flask.ext.navigation.navbar.NavigationBar
.. autoclass:: flask.ext.navigation.item.Item

Utilities
~~~~~~~~~

.. autofunction:: flask.ext.navigation.utils.freeze_dict
.. autoclass:: flask.ext.navigation.utils.BoundTypeProperty
