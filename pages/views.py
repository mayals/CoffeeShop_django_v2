from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from products.models import Product


def index_view(request):
   products = Product.objects.all().filter(in_stock=True)
   context = {
      'title' : "Index Page",
      'products' : products ,
        
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




@login_required(login_url='users:signin')
def dashboard_view(request):
   if request.user.is_authenticated and request.user.is_superuser:
      products = Product.objects.all()
      context = {
         'products' : products 
         }
      return render(request,'pages/dashboard.html',context)
   
   else:
      messages.warning(request,f'(only admin has permission to this page !')
      return HttpResponseRedirect(reverse('pages:index'))
   

  
   



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