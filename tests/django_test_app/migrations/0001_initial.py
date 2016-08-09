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
                    choices=[('spam', 'Spam'), ('bacon', 'Bacon'), ('eggs', 'Eggs')],
                    blank=True,
                    default='', )),
                ('flags', extypes.django.SetField(
                    choices=[('clean', 'clean'), ('online', 'online'), ('open', 'open')],
                    blank=True,
                    default='', )),
            ],
        ),

    ]
