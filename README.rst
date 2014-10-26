extypes
=======

This project provides a few enhanced types for Python:

* A "constrained set" (ordered or not)
* That's all for now.


It also provides extensions for Django.


It has been fully tested with all versions of Python from 2.6 to 3.4; and is distributed under the BSD license.


Links
-----

* Package on PyPI: http://pypi.python.org/pypi/extypes
* Repository and issues on GitHub: http://github.com/rbarrois/extypes
* Doc on http://readthedocs.org/docs/extypes/


Getting started
---------------

Intall the package from `PyPI`_, using pip:

.. code-block:: sh

    $ pip install extypes

Or from GitHub:

.. code-block:: sh

    $ git clone git://github.com/rbarrois/extypes
    $ cd extypes
    $ python setup.py install


To check that everything went fine, fire a Python shell and import ``extypes``:


.. code-block:: python

    import extypes


Introduction
------------

.. currentmodule:: extypes

``extypes`` provides a new type, ``ConstrainedSet``.

This is a ``set()``-like object, but values can only be taken from a
specific set of options.


A ``ConstrainedSet`` is declared in a manner very similar to :class:`collections.namedtuple`:

.. code-block:: python

    import extypes
    Foods = extypes.ConstrainedSet(['eggs', 'spam', 'bacon'])

This will declare a new class, ``Foods``, whose instances are ``ConstrainedSet`` that only accept
options among ``'eggs'``, ``'spam'`` and ``'bacon'``.


Those objects can be used as simple ``set()`` objects:

.. code-block:: pycon

    >>> import extypes
    >>> Foods = extypes.ConstrainedSet(['eggs', 'spam', 'bacon'])
    >>> meat = Foods(['spam', 'bacon'])
    >>> fresh = Foods(['bacon', 'eggs'])
    >>> 'eggs' in meat
    False
    >>> 'eggs' in fresh
    True
    >>> meat & fresh
    Foods(['bacon'])

As a ``set()`` object, they are mutable:

.. code-block:: pycon

    >>> import extypes
    >>> Foods = extypes.ConstrainedSet(['eggs', 'spam', 'bacon'])
    >>> meat = Foods(['spam', 'bacon'])
    >>> meat.remove('spam')
    >>> meat
    Foods(['bacon'])

And iterable:

.. code-block:: pycon

    >>> import extypes
    >>> Foods = extypes.ConstrainedSet(['eggs', 'spam', 'bacon'])
    >>> meat = Foods(['bacon', 'spam'])
    >>> list(meat)
    ['spam', 'bacon']

But only valid options are accepted:

.. code-block:: pycon

    >>> Foods = extypes.ConstrainedSet(['eggs', 'spam', 'bacon'])
    >>> greens = Foods(['spinach']
    Traceback (most recent call last):
    ...
    ValueError: Invalid keys ['spinach'], please use a value in ['spam', 'bacon', 'eggs'].


Extensions: Django
------------------

.. currentmodule:: extypes.django

``extypes`` also provides custom fields for Django:

.. class:: extypes.django.SetField(choices, ...)

    A :class:`SetField` wraps a :class:`~extypes.ConstrainedSet`.

    Its ``choices`` argument **MUST** be a list of two-tuples, or an existing
    :class:`~extypes.ConstrainedSet` subclass.



