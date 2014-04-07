import operator


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
