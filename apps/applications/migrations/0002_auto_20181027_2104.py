# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-27 21:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0003_resume_city'),
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='tenant',
        ),
        migrations.AddField(
            model_name='application',
            name='resume',
            field=models.ManyToManyField(to='resumes.Resume'),
        ),
    ]