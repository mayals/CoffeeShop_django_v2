from django import forms
from .models import Product


# ----- add product form --------#
class CreateProductForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=100,required=True, disabled=False)
    description = forms.CharField(label='Description',
                                min_length=300,
                                help_text='the min length of this field is 2000',
                                widget = forms.Textarea(attrs={'rows': 5, 'placeholder': 'describe the product here .. '}))
    class Meta:
        model = Product
        fields = ['name','description','price','photo','in_stock','publish_date'] 