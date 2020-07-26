from django.shortcuts import render
from rest_framework import viewsets, status

from shop.services.сart import Cart
from store.models import OrderItemModel
from rest_framework.decorators import action
from shop.services.product import Product
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import ProductSerializer, CartSerializer
import json

class ProductViewSet(viewsets.ViewSet):
    serializer = ProductSerializer
    lookup_field = 'sku'

    def list(self, request: Request):
        products = [self.serializer(product).data for product in Product.get_all()]
        return Response(products)

    def retrieve(self, request: Request, sku=None):
        product = Product.get_product_by_sku(sku=sku)
        return Response(self.serializer(product).data)


class CartViewSet(viewsets.ViewSet):
    serializer = CartSerializer

    def list(self, request: Request):
        cart = Cart(user=request.user, session=request.session)
        serializer = self.serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def quantity_of_items(self, request: Request):
        cart = Cart(request.user, request.session)
        return Response({'total_quantity': cart.quantity_of_items}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def add_item(self, request: Request):
        cart = Cart(request.user, request.session)
        cart.add_item(request.data['sku'])
        return Response({'success': 'item was added'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['patch'])
    def remove_item(self, request: Request):
        cart = Cart(request.user, request.session)
        cart.remove_item(request.data['sku'])
        return Response({'success': 'item was removed'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['patch'])
    def set_amount_of_items(self, request: Request):
        cart = Cart(request.user, request.session)
        cart.set_amount_of_items(sku=request.data['sku'], amount=request.data['amount'])
        return Response({'success': 'item was set'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['patch'])
    def clear_cart(self, request: Request):
        cart = Cart(request.user, request.session)
        cart.clear()
        return Response({'success': 'cart was cleared'}, status=status.HTTP_204_NO_CONTENT)