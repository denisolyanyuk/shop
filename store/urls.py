from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('product/<str:SKU>', views.product_details, name='product_details'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('', views.store, name='store'),
]