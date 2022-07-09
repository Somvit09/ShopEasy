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
    data = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', data)


def product_details(request, category_slug=None, product_slug=None):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug) # __ to get the slug
        # from the category model
        # by the category in Product model
    except Exception as e:
        raise e
    data = dict(single_product=single_product)
    return render(request, 'store/product-detail.html', data)
