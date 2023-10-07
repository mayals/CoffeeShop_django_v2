from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse 
from .forms import OrderProductCartForm, ShippingAdressForm, PaymentModeForm
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




 




########################################## cart_view ######################################################
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






########################################## checkout_view ######################################################
@login_required(login_url='users:signin')
def checkout_view(request,order_id):
    order = get_object_or_404(Order,user=request.user,finish=False,id=order_id) 
    orderproducts = OrderProduct.objects.all().filter(order=order)
    form = PaymentModeForm()

    context = {
        'title'         : 'Checkout Page', 
        'order'         : order,
        'orderproducts' : orderproducts,
        'form'          : form
    }    
    return render(request,'ecommerce/checkout.html', context)



########################################## edit shipping address ######################################################
@login_required(login_url='users:signin')
def editaddress_view(request,order_id):
    order = get_object_or_404(Order,user=request.user,finish=False,id=order_id) 
    form = ShippingAdressForm(instance = order)
    if request.method == 'POST':
        form = ShippingAdressForm(request.POST,instance=order)
        #print(form)
        if form.is_valid():
            u_order= form.save(commit = True)
            
            # this fields values no change only given from instance order(constant values for  current order) 
            u_order.id =  order.id
            u_order.user = order.user
            u_order.total_amount = order.total_amount
            u_order.order_date = order.order_date
            u_order.finish = False
            # get values of many to many field, orderproducts list for current order
            listorderproducts = OrderProduct.objects.filter(order=order)
            u_order.orderproducts.set(listorderproducts) # use set() with many to many

            # edit Shipping Adress (updated value) -- new value insert by user
            u_order.country = form.cleaned_data.get("country")
            u_order.city = form.cleaned_data.get("city")
            u_order.zip_code = form.cleaned_data.get("zip_code")
            u_order.state = form.cleaned_data.get("state")
            u_order.street = form.cleaned_data.get("street")
            u_order.phone_no = form.cleaned_data.get("phone_no")
            u_order.save()
            messages.success(request, f'thanks ( {request.user.first_name} ),Edit done successfully !')
            return redirect('ecommerce:checkout-view', order_id = order.id )

        else:
            messages.warning(request,f'shipping address of {request.user.first_name} Not updated !')
            form = ShippingAdressForm(request.POST,instance=order)   
    
    context = {
        'title'   :'Edit Address Page', 
        'order'   : order,
        'form'    : form ,    
    }    
    return render(request,'ecommerce/edit_address.html', context)


        
########################################## Add Payment Mode ######################################################
@login_required(login_url='users:signin')
def add_payment_mode(request,order_id):
    print('hello')
    order = get_object_or_404(Order,user=request.user,finish=False,id=order_id) 
    print("order=" + str(order))


    if request.method == 'POST':
        form= PaymentModeForm(request.POST)
        if form.is_valid():
            payment_mode = request.POST.get('payment_mode')
            print(payment_mode)
            if payment_mode == 'CARD' :
                order.payment_mode = 'CARD'
                order.save()
                messages.success(request, f'successfully choise Card payment mode')
                return redirect('ecommerce:cart-view', order_id=order_id)
            
            if payment_mode == 'COD' :
                order.payment_mode = 'COD'
                order.save()
                messages.success(request, f'successfully choise Cash on delevry payment mode')
                return redirect('ecommerce:checkout-view', order_id=order_id)

    # context = {
    #     'title'   :'add payment mode page', 
    #     'order'   : order,
    #     'form'    : form ,    
    # }    
    # return render(request,'ecommerce/checkout.html', context)










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