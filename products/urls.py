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
    path('delete_product/<int:product_id>/',
         views.delete_product, name='delete_product'),
    path('delete_variant/<int:variant_id>/',
         views.delete_variant, name='delete_variant'),
    path('stock_management/', views.stock_management, name='stock_management'),
    path('add_discount/', views.add_discount, name='add_discount'),
    path('edit_discount/<int:discount_id>/',
         views.edit_discount, name='edit_discount'),
    path('delete_discount/<int:discount_id>/',
         views.delete_discount, name='delete_discount'),
    path('add_review/<int:product_id>/', views.add_review,
         name='add_review'),
    path('edit_review/<int:review_id>/', views.edit_review,
         name='edit_review')
]
