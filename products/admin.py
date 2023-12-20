from django.contrib import admin
from .models import Category, Product, NutritionalInfo, ProductVariant, Review


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
        'sale_price',
        'stock_count',
    )

    ordering = ('product',)


class ReviewAdmin(admin.ModelAdmin):
    """ Review admin - to adjust how it is displayed in the admin panel"""

    list_display = (
        'product',
        'user',
        'rating',
        'created_date',
        'comment',
    )

    ordering = ('product',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(NutritionalInfo, NutritionalInfoAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Review, ReviewAdmin)
