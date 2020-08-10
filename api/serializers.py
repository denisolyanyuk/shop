if __name__ == '__main__':
    import django
    django.setup()
from rest_framework import serializers
from shop.services.сart import CartItem, Cart
from shop.services.product import Product



class ProductSerializer(serializers.Serializer):
    price = serializers.FloatField(read_only=True)
    title = serializers.CharField(read_only=True)
    sku = serializers.CharField(read_only=True)
    is_digital = serializers.BooleanField(read_only=True)
    main_image = serializers.ImageField(read_only=True)


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
    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    cart_item_price = serializers.FloatField(read_only=True)


class CartSerializer(serializers.Serializer):
    cart_items = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    quantity_of_items = serializers.IntegerField(read_only=True)
    has_to_be_shipped = serializers.BooleanField(read_only=True)

    @staticmethod
    def get_cart_items(cart: Cart):
        result = []
        for item in cart.get_items():
            serializer = CartItemSerializer(item)
            result.append(serializer.data)
        return result


if __name__ == '__main__':
    import cProfile
    from store.models import CartModel
    from users.models import User
    user = User.objects.get(email='denisolyanyuk@gmail.com')
    cart = CartModel.objects.get(user=user)
    cProfile.run('for i in range(50000): CartSerializer(cart)', sort='tottime')