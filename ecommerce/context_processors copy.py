from django.http import HttpResponse
from django.shortcuts import redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order,OrderProduct
from django.contrib.auth import get_user_model 



# Not put any decorations , IT BECOME NOT WORK!
@login_required(login_url='users:signin')
def cart_quant(request):
    try:      
        user = request.user
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return HttpResponse('User does not exit!')
    try:
        order = Order.objects.all().get(user=user,finish=False)
    except:
        return HttpResponse('Order does not exit!')
    

    orderproducts = OrderProduct.objects.all().filter(order=order)
    #print(orderproducts)
    if orderproducts is not None:    
        orderproducts = order.orderproducts.all().filter(order=order)
        que = 0
        for orderproduct in orderproducts :
            que = que + orderproduct.quantity
        items_quant = que
        #items_quant = orderproducts.count()
        #print(items_quant)
        return {
            "user":user,
            "order_id" : order.id, 
            "items_quant" : items_quant,
        }
    
   
    return {
            "user":user,
            "order" : order,  
            "items_quant" : 0,
        }   
        
