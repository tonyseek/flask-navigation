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
