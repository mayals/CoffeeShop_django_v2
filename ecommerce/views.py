from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse 
from .forms import OrderProductCartForm
from .models import Product, OrderProduct, Order 


########################################## add_to_cart & create order ######################################################
@login_required(login_url='users:signin')
def add_to_cart(request, pro_id):
    user = request.user
    form = OrderProductCartForm(request.GET)       
    product = get_object_or_404(Product, id=pro_id)
    product_name = product.name
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        price_at_order = product.price   # in order to save the price of order date not current price now
        
        if Order.objects.all().filter(user=user,finish=False).exists():
            # old_order
            old_order = get_object_or_404(Order,user=user,finish=False)
            if OrderProduct.objects.all().filter(order=old_order,product_name=product_name).exists():
                orderproduct = get_object_or_404(OrderProduct,order=old_order,product_name=product_name)
                quantity = form.cleaned_data['quantity']
                orderproduct.quantity = quantity      
            else:
                orderproduct = OrderProduct.objects.create(
                                                        order = old_order,
                                                        product=product,
                                                        quantity=quantity,
                                                        price_at_order = price_at_order,
                                                        product_name = product_name
                                                        )
            
            orderproduct.save()
            orderproduct.product_amount = orderproduct.quantity * orderproduct.price_at_order
            orderproduct.save()
            messages.success(request,f'(The product {product_name} ), add to cart successfully !')
            return HttpResponseRedirect(reverse('products:product', args=[pro_id]))


        #  create new_order 
        new_order = Order.objects.create(user=user,finish=False)   
        orderproduct = OrderProduct.objects.create(
                                                    order = new_order,
                                                    product=product,
                                                    quantity=quantity,
                                                    price_at_order = price_at_order,
                                                    product_name = product_name
                                                    )
        orderproduct.save()
        messages.success(request,f'(The product {product_name} ), add to cart successfully !')
        return HttpResponseRedirect(reverse('products:product', args=[pro_id]))


    messages.warning(request,f'(The product {product_name}), Not add !')
    return HttpResponseRedirect(reverse('products:product', args=[pro_id]))




    # if request.method == 'POST':
    #     form = OrderForm(request.POST)       
    #     if form.is_valid():
    #         order = form.save(commit = False)
    #         order.user = request.user
    #         order.save(commit = False)
    #         order_id = order.id
            
            # orderproducts = OrderProduct.objects.filter(order=order_id)
            # total_amount = 0
            # for product in orderproducts :
            #     quantity = product.quantity
            #     price    = product.price
            #     product_amount = quantity*price
            #     total_amount = total_amount + product_amount
                
            # order.total_amount = order.total_amount
            # order.save(commit = True)
            


    # form = OrderForm() 

    # context = {
    #    'title' : "Create Order",
    #    'form'  : form,   
    # }    
    # return render(request,'ecommerce/create_order.html', context)



@login_required(login_url='users:signin')
def cart_view(request,order_id):
    order = get_object_or_404(Order,user=request.user,finish=False,id=order_id) 
    orderproducts = OrderProduct.objects.all().filter(order=order)
    add_to_cart_form = OrderProductCartForm()

    context = {
        'title'        : 'Cart Page', 
        'order'        : order,
        'orderproducts' : orderproducts,
        'form'         : add_to_cart_form,
    }    
    return render(request,'ecommerce/cart.html', context)




@login_required(login_url='users:signin')
def increase_quality(request,order_id,item_id):
    order = get_object_or_404(Order,id=order_id,finish=False)
    item = get_object_or_404(OrderProduct,order=order,id=item_id)
    item.quantity = item.quantity + 1
    item.save()
    item.product_amount = item.quantity * item.price_at_order
    item.save()
    return redirect('ecommerce:cart-view', order_id=order_id)


@login_required(login_url='users:signin')
def decrease_quality(request,order_id,item_id):
    order = get_object_or_404(Order,id=order_id,finish=False) 
    item = get_object_or_404(OrderProduct,order=order,id=item_id)
    if item.quantity > 0 :
        item.quantity = item.quantity - 1
        item.save()
        item.product_amount = item.quantity * item.price_at_order
        item.save()
    else:
        item.quantity = 0 
        item.delete() 
    return redirect('ecommerce:cart-view', order_id=order_id)



def delete_orderproduct(request,order_id,item_id):
    order = get_object_or_404(Order,id=order_id,finish=False) 
    item = get_object_or_404(OrderProduct,order=order,id=item_id)
    item.delete() 
    return redirect('ecommerce:cart-view', order_id=order_id)




@login_required(login_url='users:signin')
def checkout_view(request,order_id):
    order = get_object_or_404(Order,user=request.user,finish=False,id=order_id) 
    orderproducts = OrderProduct.objects.all().filter(order=order)
    #shipping_address_form = ShippingAdressForm()

    context = {
        'title'         : 'Checkout Page', 
        'order'         : order,
        'orderproducts' : orderproducts,
        #'form'          : shipping_address_form ,
    }    
    return render(request,'ecommerce/checkout.html', context)






########################################## add_to_cart & creat order ######################################################
# @login_required(login_url='users:signin')
# def update_cart_form_view(request, pro_id):
#     user = request.user
#     old_order = get_object_or_404(Order,user=user,finish=False)
#     product = get_object_or_404(Product,id=pro_id)
#     product_name = product.name
#     orderproduct=get_object_or_404(OrderProduct,order=old_order, product_name=product_name)
#     quantity = orderproduct.quantity 
#     print(quantity)
#     if request.method == 'GET':
#         form = OrderProductCartForm(request.GET,instance=orderproduct)       
#         print(form)
#         form.save(commit=True)
#         print(form)
#         quantity = request.GET['quantity']
#         orderproduct.save()
#         price_at_order = product.price   # in order to save the price of order date not current price now      
#         orderproduct.product_amount = orderproduct.quantity * orderproduct.price_at_order
#         orderproduct.save()
#         messages.success(request,f'(The product {product_name} ) quantity update successfully!')
#         return redirect('ecommerce:cart-view')

    # else:
    #     form = OrderProductCartForm(instance=orderproduct)
    #     messages.success(request,f'(The product {product_name} ) quantity not update!')
    #     return redirect('ecommerce:update-cart-form-view',pro_id=pro_id )





# def update_cart_action(request):
#     user = request.user
#     old_order = get_object_or_404(Order,user=user,finish=False)
#     product = get_object_or_404(Product,id=pro_id)
#     product_name = product.name
#     orderproduct=get_object_or_404(OrderProduct,order=old_order, product_name=product_name)
    
#     form = OrderProductCartForm(request.GET,instance=orderproduct)       
    
#     if form.is_valid():
#         quantity = form.cleaned_data['quantity']
#         price_at_order = product.price   # in order to save the price of order date not current price now      
#         orderproduct.save()
#         orderproduct.product_amount = orderproduct.quantity * orderproduct.price_at_order
#         orderproduct.save()
#         messages.success(request,f'(The product {product_name} ) quantity update successfully!')
#         return HttpResponseRedirect(reverse('ecommerce:cart-view')
