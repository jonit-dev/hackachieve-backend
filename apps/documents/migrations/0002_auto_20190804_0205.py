# Generated by Django 2.2.2 on 2019-08-04 09:05

import apps.documents.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediafile',
            name='file',
            field=models.FileField(blank=True, max_length=255, upload_to='goal', validators=[apps.documents.models.validate_file_extension]),
        ),
    ]
