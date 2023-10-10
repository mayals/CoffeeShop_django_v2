from django.shortcuts import get_object_or_404
# from django.contrib.auth.decorators import login_required -- not need 
from .models import Order,OrderProduct


# Not put any decorations , IT BECOME NOT WORK!
def cart_quant(request):
    if request.user.is_authenticated:
        user = request.user
        order = get_object_or_404(Order,user=user,finish=False)
        #print(order)
        orderproducts = OrderProduct.objects.all().filter(order=order)
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
    
    else :
        return {}