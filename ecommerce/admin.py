from django.contrib import admin
from .models import Order, OrderProduct

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderProduct)