from django.contrib import admin
from .models import ProductModel, ProductImagesModel, OrderModel, OrderItemModel, CartModel, CartItemModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImagesModel)
class ProductImagesAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(CartItemModel)
class CartItem(admin.ModelAdmin):
    pass