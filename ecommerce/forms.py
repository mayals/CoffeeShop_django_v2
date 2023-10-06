from django import forms
from .models import Order, OrderProduct
# https://pypi.org/project/django-countries/
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField

# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ('__all__')

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class OrderProductCartForm(forms.ModelForm):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    class Meta:
        model  = OrderProduct
        fields = ['quantity']




class ShippingAdressForm(forms.ModelForm):
    country  = CountryField(blank_label='(select country)').formfield(label="Country", required=True,
                                        help_text='please enter your Country name',
                                        error_messages={
                                            'required': 'reqired Country Name'},
                                            widget=CountrySelectWidget(attrs={'placeholder': 'Your City Name here ..',
                                                                              'class': 'custom-select d-block w-100' } )
                                        )                                                            
    city     = forms.CharField(max_length=15, label="City", required=True,
                                        help_text='please enter your City name',
                                        error_messages={
                                            'required': 'reqired City Name'},
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'Your City Name here ..',
                                            'class': 'form-control'})
                                        )
    state    = forms.CharField(max_length=15, label="State", required=True,
                                        help_text='please enter your State name',
                                        error_messages={
                                            'required': 'reqired State Name'},
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'Your State Name here ..',
                                            'class': 'form-control'})
                                        )
    zip_code = forms.CharField(max_length=15, label="Zip Code", required=True,
                                        help_text='please enter your Zip Code',
                                        error_messages={
                                            'required': 'reqired Zip Code'},
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'Your Zip Code here ..',
                                            'class': 'form-control'})
                                        )
    street   = forms.CharField(max_length=15, label="Street Name", required=True,
                                        help_text='please enter your Street Name',
                                        error_messages={
                                            'required': 'reqired Street Name'},
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'Your Street Name here ..',
                                            'class': 'form-control'})
                                        )
    phone_no  = PhoneNumberField(max_length=13, label="Phone Number", required=True,
                                        help_text='please enter your Phone Number',
                                        error_messages={
                                            'required': 'reqired Phone Number'},
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'Your Phone Number here ..',
                                            'class': 'form-control'})
                                        )
    # phone_no = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}), label="Phone Number", required=True) 
                                                      
    class Meta:
        model = Order
        fields = ('country', 'city', 'zip_code', 'state', 'street', 'phone_no')
        labels = {
            'country':'Country',
            'city':'City',
            'state':'State',
            'zip_code':'Zip Code',
            'street':'Street',
            'phone_no':'Phone Number'
        }


    