# Generated by Django 3.0.3 on 2020-02-15 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopee_spider', '0003_auto_20200215_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='price_max',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='price_min',
            field=models.IntegerField(null=True),
        ),
    ]
