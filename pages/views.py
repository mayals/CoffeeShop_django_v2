from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from products.models import Product
from ecommerce.models import Order,OrderProduct
from ecommerce.forms import OrderProductCartForm
from pages.models import ContactUsModel



def index_view(request):
   products = Product.objects.all().filter(in_stock=True)  
   form   = OrderProductCartForm()

   if request.user.is_authenticated:
      order = Order.objects.get(user=request.user, finish=False)
      orderproducts = OrderProduct.objects.filter(order=order)
      context = {
         'title'    : 'index Page',
         'products' :  products, 
         'form'     : form,
         'orderproducts' :  orderproducts  
      }  
   else: 
      context = {
        'title' : "Index Page",
         'products' :  products,  
         'form'     : form, 
      }       
   return render(request,'pages/index.html', context)





def about_view(request):
    context = {
       'title' : "About Page",
        
    }    
    return render(request,'pages/about.html', context)









def coffee_view(request): 
    context = {
       'title' :"Coffee Page",
        
    }    
    return render(request,'pages/coffee.html', context)




from .forms import ContactUsForm

class ContactUsView(FormView):
   template_name = 'pages/contact_us.html'
   form_class = ContactUsForm
   success_url = reverse_lazy('pages:index')
   
   def get(self, request, *args, **kwargs):
      form = self.form_class
      context = {
                "form": form
      }
      return render(request,'pages/contact_us.html', context)
   
   def post(self, request, *args, **kwargs):
        if request.method == 'POST' :
            form = ContactUsForm(request.POST)
            if form.is_valid():
                  return self.form_valid(form)
            else:
                  return self.form_invalid(form)
   
   def form_valid(self, form):
      msg = """Thank you for contact us,Cofee Shop team will replay as soon as possible."""
      request = self.request
      messages.success(request, msg)
      name =  form.cleaned_data.get("name")
      email = form.cleaned_data.get("email")
      subject = form.cleaned_data.get("subject")
      message = form.cleaned_data.get("message")
      contact = ContactUsModel.objects.create(name=name, email=email, subject=subject, message=message)
      return HttpResponseRedirect(self.get_success_url())
   
   def form_invalid(self, form):
      msg = """Error done! please try again and enter correct data in the form fields."""
      request = self.request
      messages.warning(request, msg)
      # return self.get(request)
      return self.render_to_response(self.get_context_data(form=form))






      





# FOR ADMIN OLY ##### 
@login_required(login_url='users:signin')
def dashboard_view(request):
   if request.user.is_authenticated and request.user.is_superuser:
      products = Product.objects.all()
      if products is None:
         products = []
      else:
         context = {
            'products' : products 
            }
      return render(request,'pages/dashboard.html',context)
   
   else:
      messages.warning(request,f'(only admin has permission to this page !')
      return HttpResponseRedirect(reverse('pages:index'))
   

  
   


# FOR ADMIN OLY ##### 
@login_required(login_url='users:signin')
def all_users(request):
   if request.user.is_authenticated and request.user.is_superuser:
      all_users = get_user_model().objects.all()
      context = {
       'title'  : "All users Page",
       'users'  : all_users,  
      }
      return render(request,'pages/all_users.html',context)
   else:
      messages.warning(request,f'(only admin has permission to this page !')
      return HttpResponseRedirect(reverse('pages:index'))