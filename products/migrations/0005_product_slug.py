# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20170530_0657'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='slug-field'),
        ),
    ]
