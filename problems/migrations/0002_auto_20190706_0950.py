# Generated by Django 2.2.2 on 2019-07-06 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='url',
            field=models.URLField(),
        ),
    ]