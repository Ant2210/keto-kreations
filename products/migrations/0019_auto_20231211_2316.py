# Generated by Django 3.2.23 on 2023-12-11 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_product_on_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='size',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='size_unit',
            field=models.CharField(default='g', max_length=20),
        ),
    ]
