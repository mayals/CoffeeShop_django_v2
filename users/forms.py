from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
from .models import UserProfile
## https: // pypi.org/project/django-bootstrap-datepicker-plus / 
## https: // monim67.github.io/django-bootstrap-datepicker-plus/configure / 
# from bootstrap_datepicker_plus import DatePickerInput
# https://django-bootstrap-datepicker-plus.readthedocs.io/en/latest/Getting_Started.html
from bootstrap_datepicker_plus.widgets import DatePickerInput



class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=15, label="First Name", required=True,
                                        help_text='please enter english alphabetics only for First name',
                                        error_messages={
                                            'required': 'reqired first name'},
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'First Name here ..',
                                            'class': 'form-control'})
                                        )

    last_name = forms.CharField(max_length=15, label="Last Name", required=True,
                                help_text='please enter english alphabetics only for Last Name',
                                error_messages={
                                    'required': 'reqired last name'},
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Last Name here ..',
                                    'class': 'form-control'})
                                )


    email = forms.EmailField(max_length=255, label="Email", required=True,
                                 error_messages={'required': 'required email'},
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Email here ..',
                                     'class': 'form-control'})
                                )

    password1 = forms.CharField(label='password', min_length=8, required=True,help_text='use 8 and more', widget=forms.PasswordInput())
    password2 = forms.CharField(label='password configration', min_length=8,required=True, help_text='use 8 and more', widget=forms.PasswordInput())
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', )



    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('passwords not identical')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if get_user_model().objects.filter(email=cd['email']).exists():
            raise forms.ValidationError('this email used by another user')
        return cd['email']
    



class UserLoginForm(forms.ModelForm):
    class Meta:
        model   = get_user_model()
        fields  = ("email", "password")
        widgets = {
            "password": forms.PasswordInput(),
        }
        




class UserProfileForm(forms.ModelForm):                        

    bio = forms.CharField(widget=forms.Textarea(attrs={
                                                        'cols': '20',
                                                        'rows': '10',
                                                        'placeholder': 'write your bio here ..',
                                                        'class': 'form-control',
                                                      }
                                                ))
       
    
    class Meta:
        model   = UserProfile
        fields  = ('bio', 'profile_image', 'date_of_birth', 'gender', 'phone_number', 'address', 'city', 'state', 'country')
        widgets = {
            'date_of_birth': DatePickerInput(options={"format": "DD/MM/YYYY"}),
        }