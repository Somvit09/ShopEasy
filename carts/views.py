from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem


# Create your views here.

def _cart_id(request):
    cart_item_session_key = request.session.session_key
    if not cart_item_session_key:
        cart_item_session_key = request.session.create()
    return cart_item_session_key


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart_id = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart_id = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart_id.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart_id)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart_id,
            quantity=1,
        )
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total += (item.product.price) * item.quantity
            quantity += item.quantity
        tax = int(total * (2.25/100))
        grand_total = int(tax + total)
    except ObjectNotExist:
        pass
    data = dict(
        total=total,
        quantity=quantity,
        cart_items=cart_items,
        tax=tax,
        grand_total=grand_total,
    )
    return render(request, 'cart.html', data)