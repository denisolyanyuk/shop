import os


from users.models import User
from django.db import models

# Create your models here.


def get_image_subdirectory_for_item_images(instance, filename) -> str:
    return os.path.join(instance.SKU, filename)


class Product(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=7)
    main_image = models.ImageField(upload_to=get_image_subdirectory_for_item_images)
    title = models.CharField(max_length=50)
    SKU = models.CharField(max_length=20, unique=True)
    digital = models.BooleanField(default=False)


class ProductImages(models.Model):
    image = models.ImageField(upload_to=get_image_subdirectory_for_item_images)
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="secondary_images")



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.order_items.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.order_items.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        for item in self.order_items.all():
            if not item.product.digital:
                return True
        return False

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], condition=models.Q(complete=False), name='one_non_completed_order')
        ]

    def __int__(self):
        return 42


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items", default=None, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items", default=None, blank=True)
    quantity = models.IntegerField(default=0)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zip_code = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address