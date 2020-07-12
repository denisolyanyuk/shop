from django.contrib import admin
from .models import ProductModel, ProductImagesModel, OrderModel, OrderItemModel


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
