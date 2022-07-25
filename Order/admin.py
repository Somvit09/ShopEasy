from django.contrib import admin
from .models import Payment, Order, Order_product
# Register your models here.

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(Order_product)
