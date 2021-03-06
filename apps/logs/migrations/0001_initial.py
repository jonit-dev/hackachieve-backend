# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-15 05:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(max_length=255)),
                ('emitter', models.IntegerField(default=None)),
                ('target', models.IntegerField(default=None)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
