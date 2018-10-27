# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-27 17:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('properties', '0011_property_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property', models.ManyToManyField(to='properties.Property')),
                ('tenant', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
