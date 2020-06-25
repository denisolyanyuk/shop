from django.db import models

# Create your models here.


class Item(models.Model):
    price = models.PositiveSmallIntegerField()
    main_image = models.ImageField()
    title = models.CharField(max_length=50)


class ItemImages(models.Model):
    image = models.ImageField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


