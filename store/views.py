from django.shortcuts import render


def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)


def store(request):
    context = {}
    return render(request, 'store/store.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)