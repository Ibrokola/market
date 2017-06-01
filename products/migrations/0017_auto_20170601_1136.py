# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 17:36
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20170601_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='media',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/ibrokola/Desktop/PersonalProjects/toLaunch/Oja/src/live-static/protected-root'), upload_to=products.models.download_media_location),
        ),
    ]
