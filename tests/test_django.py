#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This code is distributed under the two-clause BSD License.

from __future__ import absolute_import, unicode_literals

import unittest

import extypes

from .setup_django import django_loaded

if django_loaded:  # pragma: no cover
    from extypes import django as django_extypes
    from .django_test_app import models
    import django
    from django.core.management import call_command
    from django.db import connection
    from django.test import TestCase as DjangoTestCase
    from django.test import TransactionTestCase
    from django.test import runner as django_test_runner
    from django.test import utils as django_test_utils
    from django import forms as django_forms

else:
    DjangoTestCase = unittest.TestCase


test_state = {}


def setUpModule():
    if not django_loaded:  # pragma: no cover
        raise unittest.SkipTest("Django not installed")
    django_test_utils.setup_test_environment()
    runner = django_test_runner.DiscoverRunner()
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

        fridge3 = models.Fridge(contents=[])
        fridge3.save()

        fridge3 = models.Fridge.objects.get(pk=fridge3.pk)
        self.assertEqual([], list(fridge3.contents))

        fridge4 = models.Fridge.objects.create(contents=[])
        fridge4 = models.Fridge.objects.get(pk=fridge4.pk)
        self.assertEqual([], list(fridge4.contents))

        list(models.Fridge.objects.all())


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
class SetFieldMigrationTests(DjangoTestCase):
    def test_modelstate(self):
        field = django_extypes.SetField(
            choices=[
                ('spam', "Spam"),
                ('bacon', "Bacon"),
                ('eggs', "Eggs"),
            ],
            blank=True,
        )
        self.assertEqual(
            field.deconstruct()[3],
            {'blank': True, 'choices': [('spam', 'spam'), ('bacon', 'bacon'), ('eggs', 'eggs')]},
        )


@unittest.skipIf(not django_loaded, "Django not installed")
class SetFieldMigrateTests(TransactionTestCase):
    def test_migrate(self):
        # Let's check that this does not crash
        call_command('makemigrations', verbosity=0)
        call_command('migrate', verbosity=0)
        with connection.cursor() as cursor:
            table_list = connection.introspection.get_table_list(cursor)
            if django.VERSION[:2] >= (1, 8):
                table_list = [t.name for t in connection.introspection.get_table_list(cursor)]
            self.assertIn('django_test_app_fridge', table_list)


if __name__ == '__main__':
    unittest.main()
