# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import extypes.django


class Migration(migrations.Migration):

    operations = [

        migrations.CreateModel(
            "Fridge",
            [
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('contents', extypes.django.SetField(
                    choices=[(b'spam', b'Spam'), (b'bacon', b'Bacon'), (b'eggs', b'Eggs')],
                    blank=True,
                    default='', )),
                ('flags', extypes.django.SetField(
                    choices=[(b'clean', b'clean'), (b'online', b'online'), (b'open', b'open')],
                    blank=True,
                    default='', )),
            ],
        ),

    ]
