# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import extypes.django


class Migration(migrations.Migration):

    dependencies = [
        ('django_test_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fridge',
            name='contents',
            field=extypes.django.SetField(
                choices=[(b'spam', b'Spam'), (b'bacon', b'Bacon'), (b'eggs', b'Eggs')], blank=True,),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fridge',
            name='flags',
            field=extypes.django.SetField(
                choices=[(b'clean', b'clean'), (b'online', b'online'), (b'open', b'open')], blank=True),
            preserve_default=True,
        ),
    ]
