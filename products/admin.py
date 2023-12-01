from django.contrib import admin
from .models import Category, Product, NutritionalInfo, ProductVariant


class CategoryAdmin(admin.ModelAdmin):
    """ Category admin - to adjust how it is displayed in the admin panel"""

    list_display = (
        'friendly_name',
        'name',
    )

    ordering = ('friendly_name',)


class ProductAdmin(admin.ModelAdmin):
    """ Product admin - to adjust how it is displayed in the admin panel"""

    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
        'portion_size',
        'portion_unit',
        'sale_price',
        'sale',
        'new',
        'stock_count',
    )

    ordering = ('sku',)


class NutritionalInfoAdmin(admin.ModelAdmin):
    """
    Nutritional info admin - to adjust how it is displayed in the admin panel
    """

    list_display = (
        'product',
    )

    ordering = ('product',)


class ProductVariantAdmin(admin.ModelAdmin):
    """
    Product variant admin - to adjust how it is displayed in the admin panel
    """

    list_display = (
        'product',
        'sku',
        'size',
        'price',
        'stock_count',
    )

    ordering = ('product',)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(NutritionalInfo)
admin.site.register(ProductVariant)
