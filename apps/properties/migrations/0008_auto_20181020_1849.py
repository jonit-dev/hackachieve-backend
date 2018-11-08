# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-20 18:49
from __future__ import unicode_literals

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0007_auto_20181020_1845'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='type_id',
            new_name='type',
        ),
        migrations.AlterField(
            model_name='property',
            name='upload',
            field=stdimage.models.StdImageField(blank=True, upload_to='static/images/properties/<function property_directory_path at 0x7f95228b31e0>'),
        ),
    ]