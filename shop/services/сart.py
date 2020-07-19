from abc import ABC, abstractmethod
from store.models import CartModel, CartItemModel
from users.models import User
from .product import ProductFactory, Product
from django.contrib.sessions.backends.db import SessionBase
from typing import List


class CartItem:
    def __init__(self, product: Product, quantity: int, price: float):
        self.product = product
        self.quantity = quantity
        self.price = price

    def get_total(self) -> float:
        return self.price * self.quantity


class BaseCartStorage(ABC):

    @abstractmethod
    def get_items(self) -> List[CartItem]:
        pass

    @abstractmethod
    def add_item(self, sku: str):
        pass

    @abstractmethod
    def remove_item(self, sku: str):
        pass

    def get_total_price(self) -> float:
        return sum([item.get_total() for item in self.get_items()])

    def get_amount_of_items(self) -> float:
        return sum([item.quantity for item in self.get_items()])

    @property
    def has_to_be_shipped(self) -> bool:
        for item in self.get_items():
            if not item.product.is_digital:
                return True
        return False


class SessionCartStorage(BaseCartStorage):
    def __init__(self, session: SessionBase):
        if 'cart' not in session:
            session['cart'] = {}
            session.save()
        self._storage = session['cart']
        self._session = session

    def get_items(self) -> List[CartItem]:
        result = []
        for sku, item in self._storage.items():
            product = ProductFactory.get_product_by_sku(sku)
            result.append(CartItem(
                product=product,
                price=product.price,
                quantity=item['quantity']
            ))
        return result

    def add_item(self, sku: str):
        if sku in self._storage:
            self._storage[sku]['quantity'] = int(self._storage[sku]['quantity']) + 1
        else:
            self._storage[sku] = {'quantity': 1}
        self._session.save()

    def remove_item(self, sku: str):
        if int(self._storage[sku]['quantity']) > 1:
            self._storage[sku]['quantity'] = int(self._storage[sku]['quantity']) - 1
        else:
            self._storage.pop(sku)
        self._session.save()

    def set_amount_of_items(self, sku: str, amount: int):
        if amount < 1:
            self._storage.pop(sku)
        else:
            self._storage[sku] = {'quantity': amount}
        self._session.save()

    def clear(self):
        self._session['cart'] = {}


class DBCartStorage(BaseCartStorage):
    def __init__(self, user):
        self._cart_model, created = CartModel.objects.get_or_create(user=user)
        self._user = user

    def get_items(self) -> List[CartItem]:
        return [CartItem(
            product=model.product,
            price=model.price,
            quantity=model.quantity)
            for model in self._cart_model.cart_items.all()]

    def add_item(self, sku: str):
        product = ProductFactory.get_product_by_sku(sku=sku)
        cart_item, created = CartItemModel.objects.get_or_create(product=product,
                                                                 cart=self._cart_model,
                                                                 price=product.price)
        cart_item.quantity += 1
        cart_item.save()

    def remove_item(self, sku: str):
        product = ProductFactory.get_product_by_sku(sku=sku)
        cart_item, created = CartItemModel.objects.get_or_create(product=product, cart=self._cart_model, price=product.price)
        if cart_item.quantity <= 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

    def set_amount_of_items(self, sku: str, amount: int):
        product = ProductFactory.get_product_by_sku(sku=sku)
        cart_item, created = CartItemModel.objects.get_or_create(product=product, cart=self._cart_model, price=product.price)
        if amount <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = amount
            cart_item.save()

    def clear(self):
        self._cart_model.cart_items.all().delete()


class Cart:
    def __init__(self, user: User, session: SessionBase):
        if user.is_authenticated:
            self._storage = DBCartStorage(user)
            if 'cart' in session and len(session['cart']) != 0:
                session_cart = SessionCartStorage(session)
                for item in session_cart.get_items():
                    self._storage.set_amount_of_items(item.product.sku, item.quantity)
                session_cart.clear()
        else:
            self._storage = SessionCartStorage(session)

    def add_item(self, sku: str):
        self._storage.add_item(sku)

    def remove_item(self, sku: str):
        self._storage.remove_item(sku)

    def set_amount_of_items(self, sku: str, amount: int):
        self._storage.set_amount_of_items(sku, amount)

    def get_items(self) -> List[CartItem]:
        return self._storage.get_items()

    def get_total_price(self) -> float:
        return self._storage.get_total_price()

    def get_amount_of_items(self) -> float:
        return self._storage.get_amount_of_items()

    @property
    def has_to_be_shipped(self) -> bool:
        return self._storage.has_to_be_shipped

    def clear(self):
        self._storage.clear()




