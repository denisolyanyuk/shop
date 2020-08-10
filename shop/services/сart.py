
import datetime
import time
from pprint import pprint

from django.db.models import Prefetch

if __name__ == '__main__':
    import django
    django.setup()


from django.core.exceptions import ObjectDoesNotExist
from store.models import CartModel, CartItemModel, ProductModel
from users.models import User
from shop.services.product import Product
from django.contrib.sessions.backends.db import SessionBase, SessionStore
from typing import List, Union


class CartItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def __add__(self, other: 'CartItem'):
        if self.product.sku != other.product.sku:
            raise Exception(f"Cannot add cart items with different SKU's: {self.product.sku} and {other.product.sku}")
        else:
            return CartItem(product=self.product, quantity=self.quantity+other.quantity)

    @property
    def cart_item_price(self) -> float:
        return self.product.price * self.quantity


class SessionCartStorage:
    def __init__(self, session: SessionBase):
        if 'cart' not in session:
            session['cart'] = {}
            session.save()
        self._storage = session['cart']
        self._session = session  # храним для очистки корзины

    def __contains__(self, item: CartItem):
        return item.product.sku in self._storage

    def get_items(self) -> List[CartItem]:
        result = []
        for sku, item in self._storage.items():
            product = Product.get_product_by_sku(sku)
            result.append(CartItem(
                product=product,
                quantity=item['quantity']
            ))
        return result

    def get_item_by_sku(self, sku: str) -> Union[CartItem, None]:
        if sku in self._storage:
            product = Product.get_product_by_sku(sku)
            quantity = self._storage[sku]['quantity']
            return CartItem(product=product, quantity=quantity)
        else:
            return None

    def add_item(self, sku: str, quantity: int):
        if sku in self._storage:
            self._storage[sku]['quantity'] = int(self._storage[sku]['quantity']) + quantity
        else:
            self._storage[sku] = {'quantity': quantity}
        self._session.save()

    def remove_item(self, sku: str):
        if int(self._storage[sku]['quantity']) > 1:
            self._storage[sku]['quantity'] = int(self._storage[sku]['quantity']) - 1
        else:
            self._storage.pop(sku)
        self._session.save()

    def set_quantity_of_items(self, sku: str, quantity: int):
        if quantity < 1:
            self._storage.pop(sku)
        else:
            self._storage[sku] = {'quantity': quantity}
        self._session.save()

    def clear(self):
        self._session['cart'] = {}


class DBCartStorage:
    def __init__(self, user):
        if CartModel.objects.filter(user=user).exists():
            cart_model = CartModel.objects.get(user=user)
            self._cart_model = cart_model
            self._query_cart_items = CartItemModel.objects.filter(cart=cart_model).select_related('cart', "product")
        else:
            self._cart_model = CartModel.objects.create(user=user)
        self._user = user

    def __contains__(self, item: CartItem):
        return self._cart_model.cart_items.filter(product=item.product).exists()

    def get_items(self) -> List[CartItem]:
        return [CartItem(
            product=model.product,
            quantity=model.quantity)
            for model in self._query_cart_items.all()]

    def get_item_by_sku(self, sku: str) -> Union[CartItem, None]:
        try:

            cart_item = self._query_cart_items.get(product=sku)
            return CartItem(product=cart_item.product, quantity=cart_item.quantity)
        except ObjectDoesNotExist:
            return None

    def add_item(self, sku: str, quantity: int):
        cart_item, created = self._query_cart_items.get_or_create(product=sku)
        cart_item.quantity += quantity
        cart_item.save(update_fields=['quantity'])

    def remove_item(self, sku: str):
        cart_item, created = self._cart_model.cart_items.get_or_create(product=sku)
        if cart_item.quantity <= 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save(update_fields=['quantity'])

    def set_quantity_of_items(self, sku: str, quantity: int):
        cart_item, created = self._cart_model.cart_items.get_or_create(product=sku)
        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save(update_fields=['quantity'])

    def clear(self):
        self._cart_model.cart_items.all().delete()


class Cart:
    def __init__(self, user: User, session: SessionBase):
        if user.is_authenticated:
            self._storage = DBCartStorage(user)
            session_cart = SessionCartStorage(session)
            for item in session_cart.get_items():
                self._storage.add_item(item.product.sku, item.quantity)
            session_cart.clear()
        else:
            self._storage = SessionCartStorage(session)

    def add_item(self, sku: str, quantity: int = 1):
        self._storage.add_item(sku, quantity)

    def remove_item(self, sku: str):
        self._storage.remove_item(sku)

    def set_amount_of_items(self, sku: str, amount: int):
        self._storage.set_quantity_of_items(sku, amount)

    def get_items(self) -> List[CartItem]:
        return self._storage.get_items()

    def get_item_by_sku(self, sku: str) -> Union[CartItem, None]:
        return self._storage.get_item_by_sku(sku=sku)

    @property
    def has_to_be_shipped(self) -> bool:
        for item in self.get_items():
            if not item.product.is_digital:
                return True
        return False

    @property
    def total_price(self) -> float:
        return sum([item.cart_item_price for item in self.get_items()])

    @property
    def quantity_of_items(self) -> int:
        return sum([item.quantity for item in self.get_items()])

    def clear(self):
        self._storage.clear()


if __name__ == '__main__':
    from django.db import connection, reset_queries
    user = User.objects.get(email="denisolyanyuk@gmail.com")
    session = SessionStore()
    cart = Cart(user=user, session=session)
    reset_queries()
    start = time.perf_counter()
    cart.add_item("2")
    end = time.perf_counter()
    pprint(connection.queries)
    print(f"Finished in : {(end - start):.3f}s")








