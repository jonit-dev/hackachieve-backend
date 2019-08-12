# Generated by Django 2.2.2 on 2019-08-01 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20190801_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(default=0, null=True),
        ),
    ]