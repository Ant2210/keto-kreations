# Generated by Django 3.2.23 on 2023-12-11 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_alter_product_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='new',
            field=models.BooleanField(default=False),
        ),
    ]
