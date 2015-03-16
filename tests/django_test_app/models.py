# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This code is distributed under the two-clause BSD License.

from .. import setup_django

from django.db import models

import extypes
from extypes import django as extypes_django


flags = extypes.ConstrainedSet(['clean', 'online', 'open'])


class Fridge(models.Model):
    contents = extypes_django.SetField(
        choices=[
            ('spam', "Spam"),
            ('bacon', "Bacon"),
            ('eggs', "Eggs"),
        ],
        blank=True,
    )

    flags = extypes_django.SetField(choices=flags, blank=True)
