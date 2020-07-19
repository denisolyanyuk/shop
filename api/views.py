from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import views

from shop.services.сart import Cart
from store.models import OrderItemModel
from rest_framework.decorators import action
from shop.services.product import Product, ProductFactory
from rest_framework.response import Response
from .serializers import ProductSerializer, CartSerializer


class ProductViewSet(viewsets.ViewSet):

    def lits(self, request):
        products = [ProductSerializer(product).data for product in ProductFactory.get_all()]
        return Response(products)

    def retrieve(self, request, pk=None):
        product = ProductFactory.get_product_by_sku(sku=pk)
        return Response(ProductSerializer(product).data)


class CartViewSet(viewsets.ViewSet):
    serializer = CartSerializer

    # def list(self, request):
    #     cart = Cart(user=request.user, session=request.session)
    #     serializer = self.serializer(cart)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, format=None):
    #     cart = Cart(user=request.user, session=request.session)
    #     serializer = self.serializer(cart)
    #     return Response(serializer.data)

    def retrieve(self, request):
        print('here')
        cart = Cart(user=request.user, session=request.session)
        serializer = self.serializer(cart)
        return Response(serializer.data)

    @action(detail=True)
    def add_item(self, request, pk):
        print('here')
        return Response(ProductSerializer(ProductFactory.get_product_by_sku('1')).data)