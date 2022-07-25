from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
from .models import Order
import datetime
from django.http import HttpResponse


# Create your views here.

def place_order(request, total=0, quantity=0):
    # # at first we need to see if the user has anything in cart, if not then redirect to store
    user = request.user
    cart = CartItem.objects.filter(user=user)
    print(cart)
    if cart.count() <= 0:
        return redirect('storeHome')

    grand_total = 0
    tax = 0
    for i in cart:
        total += (i.product.price * i.quantity)
        quantity += i.quantity
    tax = total * (2.25 / 100)
    grand_total = tax + total
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
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            return redirect('checkout')

    # return render(request, 'order/place-order.html')

