# Generated by Django 3.1.7 on 2021-03-18 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0008_auto_20210318_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
