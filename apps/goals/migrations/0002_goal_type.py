# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-31 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='type',
            field=models.IntegerField(default=0),
        ),
    ]
