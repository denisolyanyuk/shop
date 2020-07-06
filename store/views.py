from django.shortcuts import render
from shop.services.сart import Cart
from .models import Product, Order, OrderItem
from django.http import Http404


def cart(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.order_items.all()
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}


    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'store/cart.html', context)


def store(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'store/store.html', context)


def checkout(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.order_items.all()
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'store/checkout.html', context)


def product_details(request, SKU=False):
    if not SKU:
        raise Http404("Product does not exist")
    context = {
        "product": Product.objects.get(SKU=SKU)
    }
    return render(request, 'store/product_details.html', context)