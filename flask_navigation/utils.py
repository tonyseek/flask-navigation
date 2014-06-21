import operator
import collections


def freeze_dict(dict_):
    """Freezes ``dict`` into ``tuple``.

    A typical usage is packing ``dict`` into hashable.

    e.g.::

        >>> freeze_dict({'a': 1, 'b': 2})
        (('a', 1), ('b', 2))
    """
    pairs = dict_.items()
    key_getter = operator.itemgetter(0)
    return tuple(sorted(pairs, key=key_getter))


def join_html_attrs(attrs):
    """Joins the map structure into HTML attributes.

    The return value is a 2-tuple ``(template, ordered_values)``. It should be
    passed into :class:`markupsafe.Markup` to prevent XSS attacked.

    e.g.::

        >>> join_html_attrs({'href': '/', 'data-active': 'true'})
        ('data-active="{0}" href="{1}"', ['true', '/'])
    """
    attrs = collections.OrderedDict(freeze_dict(attrs or {}))
    template = ' '.join('%s="{%d}"' % (k, i) for i, k in enumerate(attrs))
    return template, list(attrs.values())


class BoundTypeProperty(object):
    """This kind of property creates subclasses of given class for each
    instance.

    Those subclasses means "bound type" which be used for identifying
    themselves with blinker/Flask signals.

    e.g.::

        >>> class Foo(object):
        ...     pass
        >>> class Bar(object):
        ...     Foo = BoundTypeProperty('Foo', Foo)
        >>>
        >>> Bar.Foo
        BoundTypeProperty('Foo', Foo)
        >>> bar = Bar()
        >>> bar.Foo is Foo
        False
        >>> issubclass(bar.Foo, Foo)
        True
        >>> egg = Bar()
        >>> egg.Foo is bar.Foo
        False
        >>> egg.Foo.__bases__ == bar.Foo.__bases__ == (Foo,)
        True

    :param name: the name of this property.
    :param cls: the base class of all bound classes.
    """

    def __init__(self, name, cls):
        self.name = name
        self.cls = cls

    def __repr__(self):
        return 'BoundTypeProperty(%r, %s)' % (self.name, self.cls.__name__)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        ns = vars(instance)  # the instance namespace
        if self.name not in ns:
            ns[self.name] = type(self.name, (self.cls,), {})
        return ns[self.name]


class LazyProperty(object):
    """The property which could be assigned a lazy value with callable object.

    e.g.::

        >>> class Spam(object):
        ...     egg = LazyProperty('egg')
        ...     foo = LazyProperty('foo', default=42)
        ...     bar = LazyProperty('bar', cache=True)
        >>>
        >>> Spam.egg
        LazyProperty('egg')
        >>> spam = Spam()
        >>>
        >>> # fixed value
        >>> spam.egg
        Traceback (most recent call last):
        ...
        AttributeError: 'Spam' object has no attribute 'egg' and 'make_egg'
        >>> spam.egg = 'abc'
        >>> spam.egg
        'abc'
        >>> # lazy value
        >>> spam.egg = lambda: 'def'
        >>> spam.egg
        'def'
        >>> # default value
        >>> spam.foo
        42
        >>> spam.foo = lambda: 43
        >>> spam.foo
        43
        >>> # cached value
        >>> _flag = 'new'
        >>> spam.bar = lambda: _flag
        >>> spam.bar
        'new'
        >>> _flag = 'old'
        >>> spam.bar
        'new'
        >>> spam.make_bar()
        'old'
        >>>

    :param name: the property name, which will be the cache key if the
                 ``cache`` option is ``True``.
    :param default: the optional default value. if nothing provided (even
                    ``None``), the getting operation for missing value will
                    cause ``AttributeError``.
    :param cache: if ``True`` provided, the lazy value will only be calculated
                  once. default: ``False``.
    """

    _missing = object()

    def __init__(self, name, default=_missing, cache=False):
        self.__name__ = name
        self.default = default
        self.cache = cache

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.__name__)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        instance_ns = vars(instance)

        if self.__name__ in instance_ns:
            # final value is exists
            value = instance_ns[self.__name__]
        else:
            if self.callable_name in instance_ns:
                # callable object is exists
                value = instance_ns[self.callable_name]()
                if self.cache:
                    # caches calling result as final value
                    instance_ns[self.__name__] = value
            elif self.default is not self._missing:
                # default value is exists
                value = self.default
            else:
                # nothing could be used
                error_args = (
                    owner.__name__, self.__name__, self.callable_name)
                raise AttributeError(
                    '%r object has no attribute %r and %r' % error_args)

        return value

    def __set__(self, instance, value):
        instance_ns = vars(instance)
        instance_ns.pop(self.__name__, None)
        instance_ns.pop(self.callable_name, None)

        if callable(value):
            instance_ns[self.callable_name] = value
        else:
            instance_ns[self.__name__] = value

    @property
    def callable_name(self):
        return 'make_%s' % self.__name__
