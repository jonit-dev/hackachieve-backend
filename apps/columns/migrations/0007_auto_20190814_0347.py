# Generated by Django 2.2.2 on 2019-08-14 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('columns', '0006_column_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='deadline',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
