import datetime
import time
from pprint import pprint

from django.db import connection, reset_queries
from rest_framework import viewsets, status
from django.db import connection
from shop.services.сart import Cart
from store.models import OrderItemModel
from rest_framework.decorators import action
from shop.services.product import Product
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import ProductSerializer, CartSerializer


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
        data = serializer.data
        return Response(data)

    @action(detail=False, methods=['get'])
    def quantity_of_items(self, request: Request):
        cart = Cart(request.user, request.session)
        return Response({'data': {'total_quantity': cart.quantity_of_items}}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def add_item(self, request: Request):
        reset_queries()
        start_queries = len(connection.queries)
        start_queries = len(connection.queries)
        start = time.perf_counter()
        cart = Cart(request.user, request.session)
        cart.add_item(request.data['sku'])
        serializer = self.serializer(cart)
        end = time.perf_counter()
        end_queries = len(connection.queries)
        pprint(connection.queries)
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.3f}s")
        return Response({'success': True, 'data': {'cart': serializer.data}}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def remove_item(self, request: Request):
        cart = Cart(request.user, request.session)
        cart.remove_item(request.data['sku'])
        serializer = self.serializer(cart)
        return Response({'success': True, 'data': {'cart': serializer.data}}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def set_amount_of_items(self, request: Request):
        cart = Cart(request.user, request.session)
        cart.set_amount_of_items(sku=request.data['sku'], amount=request.data['amount'])
        serializer = self.serializer(cart)
        return Response({'success': True, 'data': {'cart': serializer.data}}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def clear_cart(self, request: Request):
        cart = Cart(request.user, request.session)
        cart.clear()
        serializer = self.serializer(cart)
        return Response({'success': True, 'data': {'cart': serializer.data}}, status=status.HTTP_200_OK)

