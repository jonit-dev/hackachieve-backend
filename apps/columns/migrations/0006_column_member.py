# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-10 02:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('columns', '0005_auto_20190625_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='member',
            field=models.ManyToManyField(related_name='column_member', to=settings.AUTH_USER_MODEL),
        ),
    ]