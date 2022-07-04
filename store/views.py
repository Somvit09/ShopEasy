from django.shortcuts import render
from .models import Product


# Create your views here.
def storeHome(request):
    products = Product.objects.all().filter(is_available=True)
    data = {
        'products': products,
    }
    return render(request, 'store.html', data)
