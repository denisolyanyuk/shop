from .сart import Cart
from store.models import OrderModel, OrderItemModel, ShippingAddressModel
from users.models import User
import datetime


class Order:
    @staticmethod
    def create_order(cart: Cart, user: User, data_from_form: dict):
        transaction_id = datetime.datetime.now().timestamp()
        order = OrderModel.objects.create(user=user, transaction_id=transaction_id, date_time=datetime.datetime.now())
        for cart_item in cart.get_items():
            OrderItemModel.objects.create(product=cart_item.product,
                                          order=order,
                                          quantity=cart_item.quantity,
                                          price=cart_item.price)
        if cart.has_to_be_shipped:
            ShippingAddressModel.objects.create(
                customer=user,
                order=order,
                address=data_from_form['address'],
                city=data_from_form['city'],
                state=data_from_form['state'],
                zip_code=data_from_form['zip_code'],
            )
        cart.clear()
