from django.shortcuts import render
from shop.services.сart import Cart
from shop.services.order import Order
from shop.services.product import ProductFactory
from django.http import Http404, HttpResponseServerError, HttpResponseBadRequest
from django.http import JsonResponse
import json


def cart(request):
    cart = Cart(request.user, request.COOKIES)
    context = {
        'cart': cart
    }
    return render(request, 'store/cart.html', context)


def store(request):
    cart = Cart(user=request.user, request=request)
    products = ProductFactory.get_all()
    context = {
        'cart': cart,
        'products': products,
    }
    return render(request, 'store/store.html', context)


def checkout(request):
    cart = Cart(user=request.user, request=request)
    context = {
        'cart': cart,
    }
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    SKU = data['SKU']
    action = data['action']
    cart = Cart(user=request.user, request=request)

    if action == 'add':
        cart.add_item(SKU)
    elif action == 'remove':
        cart.remove_item(SKU)

    return JsonResponse('item was added', safe=False)


def process_order(request):
    data = json.loads(request.body)
    cart = Cart(user=request.user, request=request)
    if float(data['total']) != cart.get_total_price():
        return JsonResponse({'message': 'total price is incorrect'}, status=500)
    Order.create_order(user=request.user, cart=cart, data_from_form=data)
    return JsonResponse('order completed', safe=False)


def product_details(request, sku=''):
    if sku == '':
        raise Http404("Product does not exist")
    context = {
        "product": ProductFactory.get_product_by_sku(sku=sku)
    }
    return render(request, 'store/product_details.html', context)