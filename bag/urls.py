from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<item_id>/', views.add_to_bag, name='add_to_bag'),
    path('adjust_bag/<item_id>/', views.adjust_bag, name='adjust_bag'),
    path('remove_from_bag/<item_id>/',
         views.remove_from_bag, name='remove_from_bag'),
    path('apply_discount/', views.apply_discount, name='apply_discount'),
    path('remove_discount/', views.remove_discount, name='remove_discount'),
]
