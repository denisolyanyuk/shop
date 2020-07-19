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
    sku = serializers.CharField()
    is_digital = serializers.BooleanField()


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    is_staff = serializers.BooleanField()


class OrderItemSerializer(serializers.Serializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    price = serializers.FloatField()

class OrderSerializer(serializers.Serializer):
    user = UserSerializer()
    transaction_id = serializers.CharField()
    date_time = serializers.DateTimeField()
    order_item = OrderItemSerializer()


class CartItemSerializer(serializers.Serializer):

    quantity = serializers.IntegerField()
    price = serializers.FloatField()

class CartSerializer(serializers.Serializer):
    cart_items = serializers.SerializerMethodField()

    def get_cart_items(self, cart):
        result = []
        for item in cart.get_items():
            serializer = CartItemSerializer(item)
            result.append(serializer.data)
        return result



if __name__ == '__main__':
    product = Product(sku="1")
    serialize = ProductSerializer(product)
    data = serialize.data