# Generated by Django 3.2.23 on 2023-12-10 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='has_variants',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
