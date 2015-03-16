# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This code is distributed under the two-clause BSD License.

from __future__ import unicode_literals

from . import compat

def ConstrainedSet(choices, name=None):
    """A constrained set, where values are restricted to a set of options.

    Syntax:

    >>> MySet = ConstrainedSet(['a', 'b', 'c'], name='MySet')
    >>> x = MySet()
    >>> x.add('a')
    >>> x <= MySet(['a', 'b'])
    True

    All item-based operations will raise ``ValueError`` if the value isn't part
    of the allowed options.
    """
    if not name:
        if compat.PY2:
            name = b'ConstrainedSet'
        else:
            name = 'ConstrainedSet'

    return type(name, (BaseConstrainedSet,), {'name': name, 'choices': choices})


class BaseConstrainedSet(object):
    choices = None

    def __init__(self, initial=()):
        initial = set(initial)
        self._validate_choices(initial)
        self.enabled_choices = initial

    def _validate_choices(self, values):
        invalid_keys = set(values) - set(self.choices)
        if invalid_keys:
            raise ValueError("Invalid keys %r, please use a value from %s." %
                (list(sorted(invalid_keys)), list(self.choices)))

    # Dict-like

    def keys(self):
        return [key for key in self.choices if key in self.enabled_choices]

    def values(self):
        """Retrieve the values associated with the keys.

        Only supported if the choices are a dict.
        """
        return [value for key, value in self.choices.items() if key in self.enabled_choices]

    def items(self):
        """Retrieve the items associated with the keys.

        Only supported if the choices are a dict.
        """
        return [(key, value) for key, value in self.choices.items() if key in self.enabled_choices]

    def __getitem__(self, key):
        self._validate_choices([key])
        if key not in self.enabled_choices:
            raise KeyError("Key %r not in %r" % (key, self.enabled_choices))
        return self.choices[key]

    # Extra

    # ~ self
    def __invert__(self):
        return self.__class__(set(self.choices) - self.enabled_choices)

    # Dict & set-like

    def __iter__(self):
        return iter(self.keys())

    def copy(self):
        return self.__class__(self.enabled_choices.copy())

    # Set-like

    def __len__(self):
        return len(self.enabled_choices)

    def __bool__(self):
        return bool(self.enabled_choices)

    def __nonzero__(self):
        return bool(self.enabled_choices)

    def __contains__(self, key):
        self._validate_choices([key])
        return key in self.enabled_choices

    # Set edition

    def add(self, value):
        self._validate_choices([value])
        return self.enabled_choices.add(value)

    def remove(self, value):
        self._validate_choices([value])
        return self.enabled_choices.remove(value)

    def discard(self, value):
        self._validate_choices([value])
        return self.enabled_choices.discard(value)

    def pop(self):
        return self.enabled_choices.pop()

    def clear(self):
        return self.enabled_choices.clear()

    # Inter-set methods

    def _comparable(self, other):
        return isinstance(other, self.__class__) and other.choices == self.choices

    def _ensure_comparable(self, other):
        if not self._comparable(other):
            raise TypeError("Can't compare %r and %r" % (self, other))

    # Comparison

    def __eq__(self, other):
        return self._comparable(other) and self.enabled_choices == other.enabled_choices

    def __ne__(self, other):
        return not self._comparable(other) or self.enabled_choices != other.enabled_choices

    def isdisjoint(self, other):
        self._ensure_comparable(other)
        return self.enabled_choices.isdisjoint(other.enabled_choices)

    def issubset(self, other):
        self._ensure_comparable(other)
        return self.enabled_choices <= other.enabled_choices

    def __le__(self, other):
        return self.issubset(other)

    def __lt__(self, other):
        return self <= other and self != other

    def issuperset(self, other):
        self._ensure_comparable(other)
        return self.enabled_choices >= other.enabled_choices

    def __ge__(self, other):
        return self.issuperset(other)

    def __gt__(self, other):
        return self >= other and self != other

    # Combination

    def union(self, other):
        self._ensure_comparable(other)
        return self.__class__(self.enabled_choices | other.enabled_choices)

    # self | other
    def __or__(self, other):
        return self.union(other)

    def intersection(self, other):
        self._ensure_comparable(other)
        return self.__class__(self.enabled_choices & other.enabled_choices)

    # self & other
    def __and__(self, other):
        return self.intersection(other)

    def difference(self, other):
        self._ensure_comparable(other)
        return self.__class__(self.enabled_choices - other.enabled_choices)

    # self - other
    def __sub__(self, other):
        return self.difference(other)

    def symmetric_difference(self, other):
        self._ensure_comparable(other)
        return self.__class__(self.enabled_choices ^ other.enabled_choices)

    # self ^ other
    def __xor__(self, other):
        return self.symmetric_difference(other)

    # Self-edition with other

    def update(self, other):
        self._ensure_comparable(other)
        self.enabled_choices |= other.enabled_choices

    # self |= other
    def __ior__(self, other):
        self.update(other)
        return self

    def intersection_update(self, other):
        self._ensure_comparable(other)
        self.enabled_choices &= other.enabled_choices

    # self &= other
    def __iand__(self, other):
        self.intersection_update(other)
        return self

    def difference_update(self, other):
        self._ensure_comparable(other)
        self.enabled_choices -= other.enabled_choices

    # self -= other
    def __isub__(self, other):
        self.difference_update(other)
        return self

    def symmetric_difference_update(self, other):
        self._ensure_comparable(other)
        self.enabled_choices ^= other.enabled_choices

    # self ^= other
    def __ixor__(self, other):
        self.symmetric_difference_update(other)
        return self

    def __repr__(self):
        return '%s(%r, %r)' % (
            self.__class__.__name__,
            self.choices,
            self.keys(),
        )

    def __str__(self):
        return ','.join(self.keys())


