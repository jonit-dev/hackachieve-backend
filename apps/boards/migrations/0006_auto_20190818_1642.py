# Generated by Django 2.2.2 on 2019-08-18 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0005_board_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='description',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
