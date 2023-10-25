from django.db.models import Count,Avg
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product, Like, Review
from .forms import CreateProductForm
from ecommerce.models import Order,OrderProduct
from ecommerce.forms import OrderProductCartForm
# https://django-hitcount.readthedocs.io/en/latest/installation.html
# https://www.youtube.com/watch?v=my3Fbuho2zw
from hitcount.views import HitCountDetailView


@login_required(login_url='users:signin')
def create_product_form_view(request):
   if request.method == 'POST':
      form = CreateProductForm(request.POST, request.FILES)
      if form.is_valid():
         form.save()
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
   
   

def search_view(request):
   context = {
       'title' : "Search Page", 
   }    
   return render(request,'products/search.html', context)





def products_view(request):
   pro = Product.objects.filter(in_stock=True)

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
   
   print('request.GET',request.GET)
   if 'SORTATZ' in request.GET:
      print('SORTATZ')
      pro = pro.order_by('name')
   
   if 'SORTRATING' in request.GET:
      print('SORTRATING')
      pro = pro.order_by('-average_rating')
  
   if 'SORTPRICELTH' in request.GET:
      print('SORTPRICELTH')
      pro = pro.order_by('price')
   
   if 'SORTPRICEHTL' in request.GET:
      print('SORTPRICEHTL')
      pro = pro.order_by('-price')
   
   if 'SORTNEWARRIVAL' in request.GET:
      print('SORTNEWARRIVAL')
      pro = pro.order_by('publish_date')
   


   form   = OrderProductCartForm()

   if request.user.is_authenticated:
      order = Order.objects.get(user=request.user, finish=False)
      orderproducts = OrderProduct.objects.filter(order=order)
      context = {
         'title'    : 'Products Page',
         'products' :  pro, 
         'form'     : form,
         'orderproducts' :  orderproducts  
      } 
   else: 
      context = {
         'title'    : 'Products Page',
         'products' :  pro, 
         'form'     : form, 
      }    
   return render(request,'products/products.html', context)






# class based view
# i userd class based views because django-hitcount (number of visitors counter) not work with function based view
from hitcount.views import HitCountDetailView

class ProductDetailView(HitCountDetailView):
   model               =  Product 
   queryset            =  Product.objects.filter(in_stock=True)
   context_object_name = 'product'
   pk_url_kwarg        = 'pro_id'
   template_name       = 'products/product.html'
   count_hit           =  True

   
   
   def get_context_data(self, **kwargs):
         # Call the base implementation first to get a context
         context = super(ProductDetailView, self).get_context_data(**kwargs)
         context["title"]   = 'Product Page',
         context["form"]    = OrderProductCartForm()
         context["reviews"] = Review.objects.filter(product=self.get_object())   # number of users who do reviews for this product
         context['pro_id']  = self.pk_url_kwarg 
         
         if self.request.user.is_authenticated:
               context["like_user"]    = Like.objects.filter(user=self.request.user,product=self.get_object())
         #       context["order"]   = Order.objects.get(user=self.request.user,finish=False) 
               return context
               
         return context





# NOT USED 
# function based view
# not used because django-hitcount(the views counter) not work with function based view
# def product_view(request,pro_id):
#    product = get_object_or_404(Product,id=pro_id)
#    # add to cart buton form for item qulity
#    add_to_cart_form = OrderProductCartForm()
   
#    # for authenticatin users only
#    if request.user.is_authenticated:
#       req_user = request.user
#       like = Like.objects.filter(user=req_user,product=product).count()
#       order = get_object_or_404(Order,user=req_user,finish=False)
#       context = {
#          'title'   : 'Product Page',
#          'product' :  product,
#          'form'    : add_to_cart_form,
#          'like'    : like,
#          'order'   : order,
#       }
#    else:
#       context = {
#             'title'   : 'Product Page',
#             'product' :  product,
#             'form'    : add_to_cart_form,
#    }    
#    return render(request,'products/product.html', context)









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





# Add like to the selected product by automaticated user only
@login_required(login_url='users:signin')
def create_product_like(request, pro_id):
   user = request.user
   product = get_object_or_404(Product, id=pro_id, in_stock=True)

   like, created = Like.objects.get_or_create(user=user, product=product)
   if created:
        like.like_status = True
        like.save()
        product.likes += 1
        product.save()
   
   else:
      if like.like_status == True :
         like.like_status = False
         like.save()
         product.likes -= 1
         product.save()
         print('now false')

      elif like.like_status == False : 
         like.like_status = True
         like.save()
         product.likes += 1
         product.save() 
         print('now true')  

   return HttpResponseRedirect(reverse('products:product', args=[pro_id]))
   




@login_required(login_url='users:signin')
def user_favorites(request,user_id):
   user = get_object_or_404(get_user_model(),id=user_id)
   likes = Like.objects.filter(user=user)
   context={
      'likes': likes,
   }
   return render(request,'products/user_favorites.html',context)



# Add rating value and reating text by authentication user only for the selected product
@login_required(login_url='users:signin')
def review_rating_product(request,pro_id):
   if request.method == 'POST':
      product = get_object_or_404(Product,id=pro_id,in_stock=True)
      user = request.user
      if Review.objects.filter(product=product,user=user).exists():
         messages.warning(request, f'Sorry({request.user.first_name}) not allowed to add more than one review for each product!')
         return redirect('products:product', pro_id=pro_id)
      else:
         rating_value = request.POST.get('rating_value')
         rating_text  = request.POST.get('rating_text')
         if rating_value is not None :
            review = Review(product=product, user=user, rating_value=rating_value, rating_text=rating_text)
            review.save()
            
            # product.reviews_count
            reviews_count = Review.objects.filter(product=product).count()
            product.reviews_count = reviews_count
            product.save()
            
            # product.average_rating
            product_reviews_aggr = product.reviews.aggregate(product_average_rating=Avg("rating_value"))
            product.average_rating = product_reviews_aggr['product_average_rating']
            product.save()
          
                     
            messages.success(request, f'thanks ( {request.user.first_name} ) for adding review !')
            return redirect('products:product', pro_id=pro_id)
         else:
            messages.warning(request,f'(Please choice rating value stars !')
            return redirect('products:product', pro_id=pro_id)
   
   messages.warning(request,f'(the review not add !')
   return HttpResponseRedirect(reverse('products:product', args=[pro_id]))
