from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, Order_product
import datetime
import json
from django.http import HttpResponse


# Create your views here.

def place_order(request, total=0, quantity=0):
    # # at first we need to see if the user has anything in cart, if not then redirect to store
    user = request.user
    cart = CartItem.objects.filter(user=user)
    if cart.count() <= 0:
        return redirect('storeHome')

    grand_total = 0
    tax = 0
    for i in cart:
        total += (i.product.price * i.quantity)
        quantity += i.quantity
    tax = int(total * (2.25 / 100))
    grand_total = int(tax + total)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')  # get the ip of the user
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            # creating order object
            order = Order.objects.get(user=user, is_ordered=False, order_number=order_number)
            instance = dict(
                order=order, cart_items=cart, total=total, grand_total=grand_total, tax=tax,
            )
            return render(request, 'order/payments.html', instance)

    return render(request, 'order/place-order.html')


def payment(request):
    body = json.loads(request.body)
    # store details in the payment model
    user = request.user
    order = Order.objects.get(user=user, order_number=body['orderId'], is_ordered=False)
    pay_obj = Payment(
        user=user,
        payment_id=body['transactionId'],
        payment_method=body['payment_method'],
        status=body['transactionStatus'],
        amount_paid=order.order_total,
    )
    pay_obj.save()
    order.payment = pay_obj
    order.is_ordered = True
    order.save()

    # now we have to save the order and payment details in order_product model

    cart_items = CartItem.objects.filter(user=user)
    for items in cart_items:
        order_product = Order_product()
        order_product.user_id = user.id
        order_product.order_id = order.id
        order_product.payment = pay_obj
        order_product.product_id = items.product_id
        order_product.quantity = items.quantity
        order_product.product_price = items.product.price
        order_product.is_ordered = True
        order_product.save()
    return render(request, 'order/payments.html')
