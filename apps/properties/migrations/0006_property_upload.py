# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-20 01:26
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0005_auto_20181020_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='upload',
            field=models.FileField(default=False, storage=django.core.files.storage.FileSystemStorage(location='/home/jonit/Personal_projects/rentalmoose/static/images/properties'), upload_to=''),
        ),
    ]