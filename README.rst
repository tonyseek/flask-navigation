|Build Status| |Coverage Status| |PyPI Version| |PyPI Downloads| |Wheel Status|

Flask-Navigation
================

Build navigation bars in your Flask application. ::

    nav.Bar('top', [
        nav.Item('Home', 'index'),
        nav.Item('Latest News', 'news', {'page': 1}),
    ])


Installation
------------

::

    $ pip install Flask-Navigation


Links
-----

- `Document <https://flask-navigation.readthedocs.org>`_
- `Issue Track <https://github.com/tonyseek/flask-navigation/issues>`_


Issues
------

If you want to report bugs or request features, please create issues on
`GitHub Issues <https://github.com/tonyseek/flask-navigation/issues>`_.


Contributes
-----------

You can send a pull reueqst on
`GitHub <https://github.com/tonyseek/flask-navigation/pulls>`_.


.. |Build Status| image:: https://travis-ci.org/tonyseek/flask-navigation.svg?branch=master,develop
   :target: https://travis-ci.org/tonyseek/flask-navigation
   :alt: Build Status
.. |Coverage Status| image:: https://img.shields.io/coveralls/tonyseek/flask-navigation/develop.svg
   :target: https://coveralls.io/r/tonyseek/flask-navigation
   :alt: Coverage Status
.. |Wheel Status| image:: https://pypip.in/wheel/Flask-Navigation/badge.svg
   :target: https://pypi.python.org/pypi/Flask-Navigation
   :alt: Wheel Status
.. |PyPI Version| image:: https://img.shields.io/pypi/v/Flask-Navigation.svg
   :target: https://pypi.python.org/pypi/Flask-Navigation
   :alt: PyPI Version
.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/Flask-Navigation.svg
   :target: https://pypi.python.org/pypi/Flask-Navigation
   :alt: Downloads
