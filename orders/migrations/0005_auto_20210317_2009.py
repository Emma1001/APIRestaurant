# Generated by Django 3.1.7 on 2021-03-17 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20210317_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='product_quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
