# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 18:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0009_product_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='managers',
            field=models.ManyToManyField(blank=True, related_name='product_managers', to=settings.AUTH_USER_MODEL),
        ),
    ]
