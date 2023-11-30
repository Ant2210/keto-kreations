from django.contrib import admin
from .models import Category, Product, NutritionalInfo, ProductVariant


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(NutritionalInfo)
admin.site.register(ProductVariant)
