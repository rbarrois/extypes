# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

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
                choices=[('spam', 'Spam'), ('bacon', 'Bacon'), ('eggs', 'Eggs')], blank=True,),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fridge',
            name='flags',
            field=extypes.django.SetField(
                choices=[('clean', 'clean'), ('online', 'online'), ('open', 'open')], blank=True),
            preserve_default=True,
        ),
    ]
