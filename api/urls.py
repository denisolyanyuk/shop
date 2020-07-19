from django.conf.urls import url
from rest_framework import routers
from .views import ProductViewSet, CartViewSet
from django.urls import path, include
from .routers import CartRouter

router = routers.DefaultRouter()
cart_router = CartRouter()
# router.register(r'product', ProductViewSet, 'product')
# router.register(r'cart', CartViewSet, 'cart')
cart_router.register(r'cart', CartViewSet, 'cart')
print(cart_router.urls)
urlpatterns = cart_router.urls

# urlpatterns = [
#     # path('', include(router.urls)),
#     url(r'cart/', CartView.as_view()),
#     url(r'cart/like', CartView.as_view({'post': 'clear'})),
# ]


