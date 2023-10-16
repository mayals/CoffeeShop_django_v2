from django.http import HttpResponse
from django.shortcuts import redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order,OrderProduct
from django.contrib.auth import get_user_model 



#warning !  Not put any decorations , if you put all project be BECOME NOT WORK !!
# because this funcution is used for every user( oathenticated and anonimized user )
def cart_quant(request):
    if request.user.is_authenticated:
        order = Order.objects.all().get(user=request.user,finish=False)
        orderproducts = OrderProduct.objects.all().filter(order=order)
        print(orderproducts)
        if orderproducts is not None:    
            orderproducts = order.orderproducts.all().filter(order=order)
            que = 0
            for orderproduct in orderproducts :
                que = que + orderproduct.quantity
            items_quant = que
            #items_quant = orderproducts.count()
            #print(items_quant)
            return {
            
                "order" : order, 
                "items_quant" : items_quant,
            }
        
    
        return {
            
                "order" : order,  
                "items_quant" : 0,
            }   
            
   
    else:
        return {

        }