from django import forms
from .models import Order, OrderProduct



# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ('__all__')

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class OrderProductCartForm(forms.ModelForm):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    class Meta:
        model = OrderProduct
        fields = ['quantity']