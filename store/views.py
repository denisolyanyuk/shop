from django.shortcuts import render
from shop.services.сart import Cart
from .models import Product, Order, OrderItem, ShippingAddress
from django.http import Http404, HttpResponseServerError, HttpResponseBadRequest
from django.http import JsonResponse
import json, datetime


def cart(request):
    cart = Cart(request)
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
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.order_items.all()
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    products = Product.objects.all()

    context = {
        'items': items,
        'order': order,
        'products': products,
    }

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


def update_item(request):
    data = json.loads(request.body)
    SKU = data['SKU']
    action = data['action']
    product = Product.objects.get(SKU=SKU)
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()
    return JsonResponse('item was added', safe=False)


def process_order(request):
    data = json.loads(request.body)
    print(data)
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        order.transaction_id = transaction_id
        if float(data['total']) != order.get_cart_total:
            return JsonResponse({'message': 'total price is incorrect'}, status=500)
        order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=request.user,
                order=order,
                address=data['address'],
                city=data['city'],
                state=data['state'],
                zip_code=data['zip_code'],
            )
    return JsonResponse('order completed', safe=False)


def product_details(request, SKU=False):
    if not SKU:
        raise Http404("Product does not exist")
    context = {
        "product": Product.objects.get(SKU=SKU)
    }
    return render(request, 'store/product_details.html', context)