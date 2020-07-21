
from rest_framework import serializers
from shop.services.сart import CartItem, Cart
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
    cart_item_price = serializers.FloatField()

class OrderSerializer(serializers.Serializer):
    user = UserSerializer()
    transaction_id = serializers.CharField()
    date_time = serializers.DateTimeField()
    order_item = OrderItemSerializer()


class CartItemSerializer(serializers.Serializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    cart_item_price = serializers.FloatField()

class CartSerializer(serializers.Serializer):
    cart_items = serializers.SerializerMethodField()
    total_price = serializers.FloatField()
    quantity_of_items = serializers.IntegerField()
    has_to_be_shipped = serializers.BooleanField()

    @staticmethod
    def get_cart_items(cart: Cart):
        result = []
        for item in cart.get_items():
            serializer = CartItemSerializer(item)
            result.append(serializer.data)
        return result

if __name__ == '__main__':
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'shop.settings'
    import django
    django.setup()
    product = Product(sku="1")
    serialize = ProductSerializer(product)
    data = serialize.data