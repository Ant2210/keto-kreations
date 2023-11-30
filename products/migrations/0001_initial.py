# Generated by Django 3.2.23 on 2023-11-30 00:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('friendly_name', models.CharField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NutritionalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('energy_kcal', models.IntegerField(blank=True, null=True)),
                ('energy_kj', models.IntegerField(blank=True, null=True)),
                ('fat', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('saturated_fat', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('carbs', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('sugar', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('protein', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('fiber', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('salt', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(blank=True, max_length=254, null=True)),
                ('name', models.CharField(max_length=254)),
                ('description', models.TextField()),
                ('ingredients', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('image_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('size', models.CharField(blank=True, max_length=254, null=True)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('sale', models.BooleanField(blank=True, default=False, null=True)),
                ('new', models.BooleanField(blank=True, default=False, null=True)),
                ('stock_count', models.IntegerField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category')),
                ('nutritional_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nutritional_infos', to='products.nutritionalinfo')),
            ],
        ),
        migrations.AddField(
            model_name='nutritionalinfo',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nutritional_infos', to='products.product'),
        ),
    ]
