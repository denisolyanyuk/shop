from django.shortcuts import render
from shop.services.сart import Cart
from .models import Product
from django.http import Http404

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)


def store(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'store/store.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)


def product_details(request, SKU=False):
    if not SKU:
        raise Http404("Product does not exist")
    context = {
        "product": Product.objects.get(SKU=SKU)
    }
    return render(request, 'store/product_details.html', context)