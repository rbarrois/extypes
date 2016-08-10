# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This code is distributed under the two-clause BSD License.


from __future__ import absolute_import, unicode_literals

"""extypes-based models for Django."""

import collections

import django
from django.db import models
from django.forms import fields as forms_fields
from django.utils import six
from django.utils.itercompat import is_iterable

import extypes
from extypes import base as extypes_base


class SetField(models.Field):
    """A SQL SET field.

    Usage:
    >>> my_field = extypes.django.SetField(['a', 'b', 'c'])
    """

    db_separator = '|'

    def __init__(self, choices, *args, **kwargs):
        if (isinstance(choices, type) and issubclass(choices, extypes_base.BaseConstrainedSet)):
            set_definition = choices
            if hasattr(choices.choices, 'items'):
                django_choices = list(choices.choices.items())
            else:
                django_choices = [(c, c) for c in choices.choices]

        else:
            if not is_iterable(choices):
                raise ValueError("choices must be an iterable of (code, human_readable) tuples; got %r" % (choices,))

            for item in choices:
                if len(item) != 2:
                    raise ValueError("choices must be an iterable of (code, human_readable) tuples; got entry %r in %r" % (item, choices))

            django_choices = choices
            set_definition = extypes.ConstrainedSet(collections.OrderedDict(django_choices))

        for opt in set_definition.choices:
            if self.db_separator in opt:
                raise ValueError("%r is forbidden in choices; found in %r"
                    % (self.db_separator, opt))

        self.django_choices = django_choices
        self.set_definition = set_definition
        kwargs['max_length'] = len(self.get_prep_value(set_definition.choices))
        super(SetField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, self.set_definition):
            return value

        if value in (None, '', b''):
            value = ()

        if isinstance(value, six.text_type):
            value = value.split(self.db_separator)

        # Remove empty options
        value = [opt for opt in value if opt.strip()]

        return self.set_definition(value)

    def from_db_value(self, value, expression, connection, context):
        """Convert from the database format.

        This should be the inverse of self.get_prep_value()
        """
        return self.to_python(value)

    def db_type(self, connection):
        """Storage in the database.

        Should go for more efficient options, though.
        """
        return 'char(%d)' % self.max_length

    def get_prep_value(self, value):
        """Convert to a simple, serializable string.

        Used for databases and serializers.

        We add self.db_separator on both sides to ease lookups.
        """
        return self.db_separator.join([''] + list(value or ()) + [''])

    def get_display(self, value):
        """Display pretty-printer."""
        # 'value' is a ConstrainedSet instance,
        # and we expect our choices to be a dict
        # => value.values() yields a list of values.
        return ", ".join(value.values())

    def contribute_to_class(self, cls, name, **kwargs):
        """Contribute to the Model subclass.

        We set our custom get_FIELD_display(),
        which returns a comma-separated list of displays; and
        add a "set_definition" attribute to the class-level attribute descriptor.
        """
        super(SetField, self).contribute_to_class(cls, name, **kwargs)

        if django.VERSION[:2] < (1, 8):
            from django.db.models.fields import subclassing
            setattr(cls, self.name, subclassing.Creator(self))

        cls_attr = getattr(cls, self.name, None)
        if django.VERSION[:2] < (1, 10) and cls_attr is None:
            cls_attr = type(str(self.attname), (object,), {'set_definition': self.set_definition})
            setattr(cls, self.attname, cls_attr)

        setattr(cls_attr, 'set_definition', self.set_definition)

        def _get_FIELD_display(instance):
            value = getattr(instance, self.attname)
            return self.get_display(value)

        setattr(cls, 'get_%s_display' % self.name, _get_FIELD_display)

    def formfield(self, **kwargs):
        """Generate a formfield.

        We'll use a TypedMultipleChoiceField, and reinject the django-formatted
        choices.
        """
        defaults = {
            'choices': self.django_choices,
            'form_class': forms_fields.TypedMultipleChoiceField,
            'choices_form_class': forms_fields.TypedMultipleChoiceField,
        }
        defaults.update(**kwargs)
        return super(SetField, self).formfield(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super(SetField, self).deconstruct()
        del kwargs['max_length']
        kwargs['choices'] = [(key, key) for key in self.set_definition.choices]
        return name, path, args, kwargs
