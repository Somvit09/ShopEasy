from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import VariationModel


# Create your views here.
def storeHome(request, category_slug=None):
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        product_count = products.count()
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    data = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', data)


def product_details(request, category_slug=None, product_slug=None):
    try:
        single_product = Product.objects.get(category__slug=category_slug,
                                             slug=product_slug)  # __ to get the slug from the foreign model Category which is
        # from the category model by the category in Product model
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    data = dict(
        single_product=single_product,
        in_cart=in_cart,
    )
    return render(request, 'store/product-detail.html', data)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(product_name__icontains=keyword.capitalize()) | Q(slug__icontains=keyword.capitalize()) |
                Q(category__slug__icontains=keyword.capitalize()) |
                Q(category__category_name__icontains=keyword.capitalize()))
            product_count = products.count()  # product_name__icontains means it will search keyword in the product name of Product model
    data = dict(products=products, product_count=product_count)
    return render(request, 'store/search-result.html', data)
