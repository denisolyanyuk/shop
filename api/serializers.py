if __name__ == '__main__':
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'shop.settings'
    import django
    django.setup()

from rest_framework import serializers
from shop.services.сart import CartItem
from shop.services.product import Product


class ProductSerializer(serializers.Serializer):
    price = serializers.FloatField()
    title = serializers.CharField()
    SKU = serializers.CharField()
    is_digital = serializers.BooleanField()




if __name__ == '__main__':
    product = Product(sku="1")
    serialize = ProductSerializer(product)
    data = serialize.data