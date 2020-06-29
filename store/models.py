from users.models import User
from django.db import models

# Create your models here.


class Item(models.Model):
    price = models.PositiveSmallIntegerField()
    main_image = models.ImageField()
    title = models.CharField(max_length=50)


def get_image_subdirectory_for_item_images(instance, filename) -> str:
    return f'{instance.item.title}/{filename}'


class ItemImages(models.Model):
    image = models.ImageField(upload_to=get_image_subdirectory_for_item_images)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="secondary_images")


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)


class OrderItem(models.Model):
    item = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="item")





