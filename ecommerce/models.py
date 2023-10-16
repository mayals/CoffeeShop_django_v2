from django.db import models

from django.conf import settings
from django.urls import reverse
import uuid 
from products.models import Product
# https://pypi.org/project/shortuuid/
from shortuuid.django_fields import ShortUUIDField 
# https://django-phonenumber-field.readthedocs.io/en/latest/#
from phonenumber_field.modelfields import PhoneNumberField
# https://pypi.org/project/django-countries/
from django_countries.fields import CountryField

# CART
class OrderProduct(models.Model):
    id               = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    order            = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='orderproducts')
    product          = models.ForeignKey('products.Product', on_delete=models.CASCADE,  null=True )
    quantity         = models.PositiveIntegerField(default=1, null=True, blank=False)
    price_at_order   = models.DecimalField(default=00.00, max_digits=10, decimal_places=2 ,blank=False)
    product_amount   = models.DecimalField(default=00.00, max_digits=10, decimal_places=2 ,blank=False)   # items price = product item quantity*product item price
    product_name     = models.CharField(max_length=200, default="", blank=True)  
    def __str__(self):
            return 'order No: '+str(self.order.id) +'--'+'user email:'+str(self.order.user.email) +'--'+"product:"+str(self.product.name)
           




class OrderStatus(models.TextChoices):
    PENDING    = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED    = 'Shipped'
    DELIVERED  = 'Delivered'
    CANCELLED  = 'Cancelled'

class PaymentStatus(models.TextChoices):
    PAID   = 'Paid'
    UNPAID = 'Unpaid' 

class PaymentMode(models.TextChoices):
    COD  = 'COD'    # Cash on Delivery
    CARD = 'CARD'   # Card of Bank

class Order(models.Model):
    id             = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)                     
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    orderproducts  = models.ManyToManyField(Product, through='OrderProduct')
    total_amount   = models.DecimalField(default=00.00, max_digits=10, decimal_places=2 ,blank=False)   # final order price = total items quantity*total items price
    order_date     = models.DateTimeField(auto_now_add=True, auto_now=False) 
    finish         = models.BooleanField(default=False, blank=True, null=True)
    
    country        = CountryField(blank_label="(select country)", multiple=False)    
    city           = models.CharField(max_length=100, default=" ", blank=False)
    zip_code       = models.CharField(max_length=100, default=" ", blank=False)
    state          = models.CharField(max_length=100, default=" ", blank=False)
    street         = models.CharField(max_length=100, default=" ", blank=False)
    phone_no       = PhoneNumberField(null=True,default=" ", blank=False)
    
    payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_mode   = models.CharField(max_length=30, choices=PaymentMode.choices, default=PaymentMode.COD)
    status         = models.CharField(max_length=60, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
    
    def __str__(self):
        return f"{self.id}"
    
    def get_absolute_url(self):
        return reverse('order-detail', kwargs = {'id':self.id}) # view_name='{model_name}-detail'
    
    class Meta:
        ordering = ('order_date',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        
    
    @property
    def orderproducts(self):
        orderproducts = OrderProduct.objects.all().filter(order = self)
        return orderproducts
    
    @property
    def get_final_amount(self):
        orderproducts = OrderProduct.objects.filter(order=self)
        result = 0
        if orderproducts is not None:  

            for item in orderproducts :
                quantity = item.quantity
                price_at_order    = item.price_at_order
                product_amount = quantity*price_at_order
                #print(product_amount)
                result = result + int(product_amount)
                print(result)
                return result
        
        return result