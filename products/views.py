from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product, Like, Review
from .forms import CreateProductForm
from ecommerce.models import Order
from ecommerce.forms import OrderProductCartForm
# https://django-hitcount.readthedocs.io/en/latest/installation.html
# https://www.youtube.com/watch?v=my3Fbuho2zw
from hitcount.views import HitCountDetailView


@login_required(login_url='users:signin')
def create_product_form_view(request):
   if request.method == 'POST':
      form = CreateProductForm(request.POST, request.FILES)
      if form.is_valid():
         form.save(commit=True)
         form = CreateProductForm()
          
         if 'saveandcontinue' in request.POST:
            messages.success(request, f'Thanks ( {request.user.first_name} ),new product add successfully!')
            return redirect('products:products')

         elif 'saveandaddanother' in request.POST:
            messages.success(request,f'Thanks ( {request.user.first_name} ),new product add successfully !')
            return redirect('products:add-new-product')

   else:
        form = CreateProductForm()   
      
   context = {
         'title' : 'Add a new product page',
         'form'  : form,
   } 
   return render(request, 'products/create_product.html', context)
   
   

def products_view(request):
   pro = Product.objects.all().filter(in_stock=True)

   # search with or without sencitve case 
   cs = None
   if 'cs' in request.GET :
      cs = request.GET['cs']
      if not cs: 
         cs = "off"
  
   # search by name
   if "schname" in request.GET :
      schname = request.GET['schname']
      if cs == "on":
         pro =  pro.filter(name__contains=schname)
      else:
         pro =  pro.filter(name__icontains=schname)
   
   # search by description
   if 'schdescription' in request.GET :
      schdescription = request.GET['schdescription']
      if cs == 'on':
         pro =  pro.filter(description__contains=schdescription)
      else:
         pro =  pro.filter(description__icontains=schdescription)

   # search by between tow prices
   if 'schprice_from' in request.GET and 'schprice_to' in request.GET:   
         schprice_from = request.GET['schprice_from']
         schprice_to = request.GET['schprice_to']
         if schprice_from.isdigit() and schprice_to.isdigit():
            pro =  pro.filter(price__gte=schprice_from,price__lte=schprice_to)
   
   context = {
      'title'    : 'Products Page',
      'products' :  pro,     
   }    
   return render(request,'products/products.html', context)






# class based view
# i userd class based views because django-hitcount (number of visitors counter) not work with function based view
from hitcount.views import HitCountDetailView

class ProductDetailView(HitCountDetailView):
   model               =  Product 
   queryset            =  Product.objects.all()
   context_object_name = 'product'
   pk_url_kwarg        = 'pro_id'
   template_name       = 'products/product.html'
   count_hit           =  True

   def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        

        # Add in a QuerySet of all the books
        if self.request.user.is_authenticated:
            print(self.request.user.is_authenticated)
            context["title"]   = 'Product Page',
            print(context["title"])
            context["form"]    = OrderProductCartForm()
            print(context["form"])
            context["reviews"] = Review.objects.filter(product=self.get_object())
            print(context["reviews"])
            context["like"]  = Like.objects.filter(user=self.request.user,product=self.get_object()).count()
            print(context["like"])
            context["order"] = get_object_or_404(Order,user=self.request.user,finish=False) 
            print(context["order"])
            # print(context)
            return context
        else:
            context["title"]   = 'Product Page',
            context["form"]    = OrderProductCartForm() 
            context["reviews"] = Review.objects.all()      
            # print(context)
            return context





# NOT USED 
# function based view
# not used because django-hitcount(the views counter) not work with function based view
def product_view(request,pro_id):
   product = get_object_or_404(Product,id=pro_id)
   # add to cart buton form for item qulity
   add_to_cart_form = OrderProductCartForm()
   
   # for authenticatin users only
   if request.user.is_authenticated:
      req_user = request.user
      like = Like.objects.filter(user=req_user,product=product).count()
      order = get_object_or_404(Order,user=req_user,finish=False)
      context = {
         'title'   : 'Product Page',
         'product' :  product,
         'form'    : add_to_cart_form,
         'like'    : like,
         'order'   : order,
      }
   else:
      context = {
            'title'   : 'Product Page',
            'product' :  product,
            'form'    : add_to_cart_form,
   }    
   return render(request,'products/product.html', context)









@login_required(login_url='users:signin')
def update_product_view(request,pro_id):
   product = get_object_or_404(Product, id=pro_id)
   if request.method == 'POST':
      form = CreateProductForm(request.POST, request.FILES, instance=product)
      if form.is_valid():
         form.save(commit=True)
         messages.success(request, f'thanks ( {request.user.first_name} ),Edit done successfully !')
         return redirect('products:product', pro_id = product.id )
    
   else:
        form = CreateProductForm(instance=product)   
      
   context = {
         'title' : 'update the product',
         'form'  : form,
   } 
   return render(request, 'products/update_product.html', context)
   




@login_required(login_url='users:signin')
def delete_product_view(request,pro_id):
   product = get_object_or_404(Product, id=pro_id)
   product.delete()
   messages.success(request, f'Delete the product done successfully !')
   return redirect('products:products')




def search_view(request):
   context = {
       'title' : "Search Page", 
   }    
   return render(request,'products/search.html', context)



@login_required(login_url='users:signin')
def create_product_like(request, pro_id):
   user = request.user
   product = get_object_or_404(Product, id=pro_id)   
   if not Like.objects.filter(user=user, product=product).exists():
      like = Like.objects.create(user=user, product=product)
      like.like_status=True
      like.save()
      product.likes = product.likes + 1
   else:
      like = Like.objects.filter(user=user, product=product)
      like.delete()
      # like.like_status=False  NOT NEED BECAUSE like is DELETED 
      # Like.objects.update(product=product)
      product.likes = product.likes - 1
   product.likes = product.likes
   product.save()
   return HttpResponseRedirect(reverse('products:product', args=[pro_id]))


@login_required(login_url='users:signin')
def user_favorites(request,user_id):
   user = get_object_or_404(get_user_model(),id=user_id)
   likes = Like.objects.filter(user=user)
   context={
      'likes': likes,
   }
   return render(request,'products/user_favorites.html',context)




@login_required(login_url='users:signin')
def review_rating_product(request,pro_id):
   if request.method == 'GET':
      product = get_object_or_404(Product,id=pro_id)
      user = request.user
      if Review.objects.filter(product=product,user=user).exists():
         messages.warning(request, f'Sorry({request.user.first_name}) not allowed to add more than one review for each product!')
         return redirect('products:product', pro_id=pro_id)
      else:
         rating_value = request.GET.get('rating_value')
         rating_text = request.GET.get('rating_text')
         review = Review(product=product, user=user, rating_value=rating_value, rating_text=rating_text)
         review.save()
         reviews_count = Review.objects.all().count()
         product.reviews_count = reviews_count
         product.save()
         messages.success(request, f'thanks ( {request.user.first_name} ) for adding review !')
         return redirect('products:product', pro_id=pro_id)

   messages.warning(request,f'(the review not add !')
   return HttpResponseRedirect(reverse('products:product', args=[pro_id]))
