import os

from users.models import User
from django.db import models

# Create your models here.

def get_image_subdirectory_for_item_images(instance, filename) -> str:
    return os.path.join(instance.SKU, filename)


class Product(models.Model):
    price = models.PositiveSmallIntegerField()
    main_image = models.ImageField(upload_to=get_image_subdirectory_for_item_images)
    title = models.CharField(max_length=50)
    SKU = models.CharField(max_length=20, unique=True)

    @property
    def main_image_url(self):
        try:
            url = self.main_image.url
        except Exception:
            url = ""
        return url

class ProductImages(models.Model):
    image = models.ImageField(upload_to=get_image_subdirectory_for_item_images)
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="secondary_images")


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)


class OrderItem(models.Model):
    item = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="item")





