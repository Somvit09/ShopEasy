from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def signin(request):
    return render(request, 'signin.html')


def register(request):
    return render(request, 'register.html')


def cart(request):
    return render(request, 'cart.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def store(request):
    return render(request, 'store.html')


def search_result(request):
    return render(request, 'search_result.html')


def product_details(request):
    return render(request, 'product-detail.html')


def order(request):
    return render(request, 'order_complete.html')


def search(request):
    return render(request, 'search-result.html')


def place_order(request):
    return render(request, 'place-order.html')