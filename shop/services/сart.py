from store.models import Product, Order, OrderItem

class CartStorage:
    def __int__(self, user):
        if user.is_authenticated:
            return 






class Cart:
    def __init__(self, request):
        self._storage = CartStorage(request.user)