#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This code is distributed under the two-clause BSD License.

from __future__ import absolute_import, unicode_literals

import unittest

import extypes

from .setup_django import django, django_loaded
from .setup_django import south, south_loaded

if django_loaded:  # pragma: no cover
    from extypes import django as django_extypes
    from .django_test_app import models
    from django.test import TestCase as DjangoTestCase
    from django.test import simple as django_test_simple
    from django.test import utils as django_test_utils
    from django import forms as django_forms

else:
    DjangoTestCase = unittest.TestCase


test_state = {}


def setUpModule():
    if not django_loaded:  # pragma: no cover
        raise unittest.SkipTest("Django not installed")
    django_test_utils.setup_test_environment()
    runner = django_test_simple.DjangoTestSuiteRunner()
    runner_state = runner.setup_databases()
    test_state.update({
        'runner': runner,
        'runner_state': runner_state,
    })


def tearDownModule():
    if not django_loaded:  # pragma: no cover
        return
    runner = test_state['runner']
    runner_state = test_state['runner_state']
    runner.teardown_databases(runner_state)
    django_test_utils.teardown_test_environment()


@unittest.skipIf(not django_loaded, "Django not installed")
class SetFieldTests(DjangoTestCase):
    def test_default_value(self):
        fridge = models.Fridge()
        self.assertEqual([], list(fridge.contents))

    def test_validation(self):
        """full_clean() should accept valid defaults."""
        # Empty
        fridge = models.Fridge()
        fridge.full_clean()

        # One item
        fridge2 = models.Fridge(contents=['spam'])
        fridge2.full_clean()

        # Two items
        fridge3 = models.Fridge(contents=['spam', 'bacon'])
        fridge3.full_clean()

        with self.assertRaises(ValueError):
            fridge4 = models.Fridge(contents=['spam', 'milk'])

    def test_choices_validation(self):
        """SetField won't accept invalid choices."""
        with self.assertRaises(ValueError):
            django_extypes.SetField(choices=[
                ('bad|bad', "OK"),
            ])

    def test_choices_with_existing_set(self):
        """SetField accepts an already-defined ConstrainedSet."""
        Foods = extypes.ConstrainedSet(
            {'eggs': "Eggs", 'spam': "Spam", 'bacon': "Bacon"},
        )
        field = django_extypes.SetField(choices=Foods)
        self.assertEqual(Foods, field.set_definition)
        self.assertEqual(Foods.choices, dict(field.django_choices))

    def test_base_operation(self):
        """A SetField field should act like a proper set."""
        fridge = models.Fridge(contents=['bacon'])
        self.assertEqual(1, len(fridge.contents))
        self.assertEqual(['bacon'], list(fridge.contents))
        self.assertTrue('bacon' in fridge.contents)

        fridge.contents.add('spam')
        self.assertEqual(['spam', 'bacon'], list(fridge.contents))
        self.assertTrue('spam' in fridge.contents)
        self.assertTrue('bacon' in fridge.contents)

        fridge.contents.remove('bacon')
        self.assertEqual(['spam'], list(fridge.contents))

        fridge.contents = ['bacon', 'eggs']
        self.assertEqual(['bacon', 'eggs'], list(fridge.contents))
        # Properly converted into a ConstrainedSet instance
        self.assertNotEqual(['bacon', 'eggs'], fridge.contents)

    def test_db_interaction(self):
        """A SetField can be saved and restored."""
        fridge = models.Fridge(contents=['bacon'])
        fridge.save()

        fridge = models.Fridge.objects.get(pk=fridge.pk)
        self.assertEqual(['bacon'], list(fridge.contents))

        fridge2 = models.Fridge(contents=['spam', 'bacon'])
        fridge2.save()

        fridge2 = models.Fridge.objects.get(pk=fridge2.pk)
        self.assertEqual(['spam', 'bacon'], list(fridge2.contents))

    def test_get_display(self):
        """A SetField should support get_FIELD_display()."""
        fridge = models.Fridge(contents=['bacon'])
        self.assertEqual("Bacon", fridge.get_contents_display())

        fridge2 = models.Fridge(contents=['bacon', 'spam'])
        self.assertEqual("Spam, Bacon", fridge2.get_contents_display())

    def test_form_field(self):
        """A SetField should appear as a MultipleSelect HTML field."""
        class MyForm(django_forms.ModelForm):
            class Meta:
                model = models.Fridge
                fields = ['contents']

        # Check form HTML
        base_form = MyForm()
        form_html = base_form.as_table()
        self.assertIn('multiple="multiple"', form_html)
        self.assertIn('contents', form_html)
        self.assertIn("eggs", form_html)
        self.assertIn("Eggs", form_html)

        # Check validation of an empty form
        empty_form = MyForm({})
        empty_form.full_clean()
        self.assertEqual({}, empty_form.errors)
        empty_fridge = empty_form.save()
        self.assertEqual([], list(empty_fridge.contents))

        # HTML/POST form: 'contents' is a list of options.
        filled_form = MyForm({'contents': ['spam', 'bacon']})
        fridge = filled_form.save()
        self.assertEqual(['spam', 'bacon'], list(fridge.contents))

        fridge = models.Fridge(contents=['spam', 'bacon'])
        prefilled_form = MyForm(instance=fridge)
        form_html = prefilled_form.as_table()
        self.assertIn('value="spam" selected="selected"', form_html)


@unittest.skipIf(not django_loaded, "Django not installed")
@unittest.skipIf(django.VERSION[:2] < (1, 7), "Migrations unavailable in Django<1.7")
class SetFieldMigrationTests(DjangoTestCase):
    def test_modelstate(self):
        from django.db.migrations import state as migrations_state
        fridge_mstate = migrations_state.ModelState.from_model(models.Fridge)
        project_state = migrations_state.ProjectState()
        project_state.add_model_state(fridge_mstate)
        apps = project_state.render()

        model = apps.get_model('django_test_app.Fridge')
        self.assertEqual(
            [('spam', 'spam'), ('bacon', 'bacon'), ('eggs', 'eggs')],
            list(model._meta.fields[1].set_definition.choices.items()),
        )

@unittest.skipIf(not django_loaded, "Django not installed")
@unittest.skipIf(not south_loaded, "South not installed")
@unittest.skipIf(django.VERSION[:2] >= (1, 7), "South isn't compatible with Django>=1.7")
class SetFieldSouthTests(DjangoTestCase):
    def test_freezing_model(self):
        import south.modelsinspector
        frozen = south.modelsinspector.get_model_fields(models.Fridge)
        self.assertEqual(
            (
                'extypes.django.SetField',  # Class
                [],  # *args
                {
                    'blank': "True",
                    'choices': [('spam', 'spam'), ('bacon', 'bacon'), ('eggs', 'eggs')],
                },
            ),
            frozen['contents'],
        )


if __name__ == '__main__':
    unittest.main()
