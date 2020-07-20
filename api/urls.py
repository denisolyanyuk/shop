from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, CartViewSet
from django.urls import path, include
from .routers import CartRouter, ProductRouter


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path(r'', include(router.urls)),
]

