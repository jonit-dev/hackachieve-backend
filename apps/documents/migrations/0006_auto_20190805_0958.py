# Generated by Django 2.2.2 on 2019-08-05 16:58

import apps.documents.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20190805_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediafile',
            name='file',
            field=models.FileField(max_length=255, upload_to='static/file', validators=[apps.documents.models.validate_file_extension]),
        ),
    ]