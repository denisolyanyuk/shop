from django.conf.urls import url
from rest_framework import routers
from .views import ProductViewSet, CartViewSet
from django.urls import path, include
from .routers import CartRouter

default_router = routers.DefaultRouter()
cart_router = CartRouter()
default_router.register(r'products', ProductViewSet, basename='products')

cart_router.register(r'cart', CartViewSet, basename='cart')

# cart_router.registry.extend(default_router.registry)
cart_router.urls.extend(default_router.urls)
for url in cart_router.urls:
    print(url)

urlpatterns = [
     path('', include(cart_router.urls)),

]


# urlpatterns = [
#     url(r'^cart/$', CartViewSet.as_view({'get': 'retrieve'})),
#     url(r'^cart/add_item/$', CartViewSet.as_view({'post': 'add_item'})),
#
# ]

