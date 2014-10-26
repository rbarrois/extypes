# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This code is distributed under the two-clause BSD License.


from django.db import models

from extypes import django as extypes_django


class Fridge(models.Model):
    contents = extypes_django.SetField(
        choices=[
            ('spam', "Spam"),
            ('bacon', "Bacon"),
            ('eggs', "Eggs"),
        ],
        blank=True,
    )
