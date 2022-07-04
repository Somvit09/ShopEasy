from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category


# Create your views here.
def storeHome(request, category_slug=None):
    categories = Category.objects.all()
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
    # data = {
    #     'products': products,
    #     'product_count': product_count,
    #     'categories': categories,
    # }
    data = dict(
        products=products, product_count=product_count, categories=categories
    )
    print(data['categories'])
    return render(request, 'store.html', data)
