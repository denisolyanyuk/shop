import datetime
from abc import ABC, abstractmethod
from store.models import ProductModel, OrderModel, OrderItemModel, CartModel, CartItemModel, ShippingAddressModel
from users.models import User


class Products:
    @staticmethod
    def get_by_sku(sku: str):
        return ProductModel.objects.get(SKU=sku)

    @staticmethod
    def get_all():
        return ProductModel.objects.all()


class CartItem:
    def __init__(self, product: ProductModel, quantity: int, price: float):
        self.product = product
        self.quantity = quantity
        self.price = price

    def get_total(self):
        return self.price * self.quantity


class BaseCartStorage(ABC):
    @abstractmethod
    def get_items(self):
        pass

    def get_total_price(self) -> float:
        return sum([item.get_total() for item in self.get_items()])

    def get_amount_of_items(self) -> float:
        return sum([item.quantity for item in self.get_items()])

    @property
    def has_to_be_shipped(self):
        for item in self.get_items():
            if not item.product.digital:
                return True
        return False

    
class CookiesCartStorage(BaseCartStorage):
    def __init__(self, cookies):
        if 'cart' in cookies:
            self._storage = cookies['cart']
        else:
            self._storage = {}

    def get_items(self):
        result = {}
        for item in self._storage:
            product = Products.get_by_sku(item['sku'])
            self._storage[item['sku']] = CartItem(
                product=product,
                price=product.price,
                quantity=item['quantity']
            )
        return result

    def add_item(self, sku: str):
        if sku in self._storage:
            self._storage[sku] = int(self._storage[sku]['quantity']) + 1
        else:
            product = Products.get_by_sku(sku)
            self._storage[sku] = CartItem(
                product=product,
                price=product.price,
                quantity=1
            )

    def remove_item(self, sku: str):
        if int(self._storage[sku]['quantity']) > 1:
            self._storage[sku]['quantity'] = int(self._storage[sku]['quantity']) - 1
        else:
            self._storage.pop(sku)

    def set_amount_of_items(self, sku: str, amount: int):
        if amount < 1:
            self._storage.pop(sku)
        else:
            self._storage[sku]['quantity'] = amount

    def clear(self):
        self._storage = {}


class DBCartStorage(BaseCartStorage):
    def __init__(self, user):
        self._cart_model, created = CartModel.objects.get_or_create(user=user)
        self._user = user

    def get_items(self):
        return {model.product.SKU: CartItem(
            product=model.product,
            price=model.price,
            quantity=model.quantity)
            for model in self._cart_model.cart_items.all()}

    def add_item(self, sku: str):
        product = Products.get_by_sku(sku=sku)
        cart_item, created = CartItemModel.objects.get_or_create(product=product,
                                                                 cart=self._cart_model,
                                                                 price=product.price)
        cart_item.quantity += 1
        cart_item.save()

    def remove_item(self, sku: str):
        product = Products.get_by_sku(sku=sku)
        cart_item, created = CartItemModel.objects.get_or_create(product=product, cart=self._cart_model)
        if cart_item.quantity <= 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

    def set_amount_of_items(self, sku: str, amount: int):
        product = Products.get_by_sku(sku=sku)
        cart_item, created = CartItemModel.objects.get_or_create(product=product, cart=self._cart_model)
        if amount <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = amount
            cart_item.save()

    def clear(self):
        self._cart_model.cart_items.all().delete()


class Cart:
    def __init__(self, user, cookies):
        if user.is_authenticated:
            self._storage = DBCartStorage(user)
        else:
            self._storage = CookiesCartStorage(cookies)

    def add_item(self, sku: str):
        self._storage.add_item(sku)

    def remove_item(self, sku: str):
        self._storage.remove_item(sku)

    def set_amount_of_items(self, sku: str, amount: int):
        self._storage.set_amount_of_items(sku, amount)

    def get_items(self):
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

