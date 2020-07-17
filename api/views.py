from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import views
from store.models import OrderItemModel
from rest_framework.decorators import action
# Create your views here.
from rest_framework.response import Response
from .serializers import ProductSerializer

class ProductView(views.APIView):

    def get(self, request):
        """
        Return a list of all users.
        """
        products = [ProductSerializer(product) for product in ]
        return Response(usernames)