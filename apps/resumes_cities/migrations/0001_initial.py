# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-27 00:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities', '0001_initial'),
        ('resumes', '0008_auto_20181226_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume_city',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities.City')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.Resume')),
            ],
        ),
    ]
