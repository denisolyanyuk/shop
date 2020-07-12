import datetime
import os


from users.models import User
from django.db import models

# Create your models here.


def get_image_subdirectory_for_item_images(instance, filename) -> str:
    return os.path.join(instance.SKU, filename)


class ProductModel(models.Model):
    price = models.FloatField()
    main_image = models.ImageField(upload_to=get_image_subdirectory_for_item_images)
    title = models.CharField(max_length=50)
    SKU = models.CharField(max_length=20, unique=True)
    digital = models.BooleanField(default=False)


class ProductImagesModel(models.Model):
    image = models.ImageField(upload_to=get_image_subdirectory_for_item_images)
    item = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="secondary_images")


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True)
    date_time = models.DateTimeField(default=datetime.datetime.now())


class OrderItemModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True, related_name="order_items", default=None, blank=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="order_items", default=None, blank=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=7)


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class CartItemModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="cart_items", default=None,
                                blank=True)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name="cart_items", default=None, blank=True)
    quantity = models.IntegerField(default=0)
    price = models.FloatField()


class ShippingAddressModel(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zip_code = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address