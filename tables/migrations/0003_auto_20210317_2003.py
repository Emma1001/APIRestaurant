# Generated by Django 3.1.7 on 2021-03-17 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0002_auto_20210316_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='table',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]