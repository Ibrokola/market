# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 12:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='member_since',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]