# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-01 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0008_auto_20181226_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='current_ocupation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='current_wage',
            field=models.FloatField(null=True),
        ),
    ]