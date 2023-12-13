from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('product_management/',
         views.product_management, name='product_management'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_variant/', views.add_variant, name='add_variant'),
    path('edit_product/<int:product_id>/',
         views.edit_product, name='edit_product'),
    path('edit_variant/<int:variant_id>/',
         views.edit_variant, name='edit_variant'),
]
