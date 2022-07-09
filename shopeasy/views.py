from django.shortcuts import render
from category.models import Category
from store.models import Product


def home(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    data = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'index.html', data)


def signin(request):
    return render(request, 'signin.html')


def register(request):
    return render(request, 'register.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def search_result(request):
    return render(request, 'search_result.html')


def order(request):
    return render(request, 'order_complete.html')


def search(request):
    return render(request, 'search-result.html')


def place_order(request):
    return render(request, 'place-order.html')
