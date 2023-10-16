from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse 
from .forms import OrderProductCartForm, ShippingAdressForm, PaymentModeForm
from .models import Product, OrderProduct, Order 
# stripe 
from django.conf import settings
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

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
    add_to_cart_form = OrderProductCartForm()
    
    try:
        order = Order.objects.get(id=order_id,user=request.user,finish=False) 
    except (TypeError, ValueError, OverflowError, Order.DoesNotExist):
        return HttpResponse('order does not exit!')
   
   
    orderproducts = order.orderproducts.all()
    
    context = {
        'title'        : 'Cart Page', 
        'order'        : order,
        'orderproducts' : orderproducts,
        'form'         : add_to_cart_form,
    }
    print(order)
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
    if item.quantity > 1 :
        item.quantity = item.quantity - 1
        item.save()
        item.product_amount = item.quantity * item.price_at_order
        item.save()
    elif  item.quantity <= 1  :
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
       

     
        if form.is_valid():
            u_order= form.save(commit=False)
            
            # this fields values no change only given from instance order(constant values for  current order) 
            u_order.id =  order.id
            u_order.user = order.user
            u_order.total_amount = order.get_final_amount
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
    #print('hello')
    order = get_object_or_404(Order,user=request.user,finish=False,id=order_id) 
    instance = order.payment_mode
    form= PaymentModeForm(instance)
    #print("order=" + str(order))
    if request.method == 'POST':
        form= PaymentModeForm(request.POST,instance)
        request.session["is_payment_mode_choosin"] = False
        if form.is_valid():
            payment_mode = request.POST.get('payment_mode')
            #print(payment_mode)
            if payment_mode == 'CARD' :
                order.payment_mode = 'CARD'
                order.save()
                messages.success(request, f'successfully choise Card payment mode')
                # request.session["is_payment_mode_choosin"] = True
                # print(request.session["is_payment_mode_choosin"])
                return redirect('ecommerce:checkout-view', order_id=order_id)
            
            if payment_mode == 'COD' :
                order.payment_mode = 'COD'
                order.save()
                messages.success(request, f'successfully choise Cash on delevry payment mode')
                # request.session["is_payment_mode_choosin"] = True
                # print(request.session["is_payment_mode_choosin"])
                return redirect('ecommerce:checkout-view', order_id=order_id)




########################################## Stripe --  card payment ######################################################
# Stripe 
# https://testdriven.io/blog/django-stripe-tutorial/
# https://stripe.com/docs/checkout/quickstart?lang=python
# https://www.youtube.com/watch?v=66joNBEyNwE&list=PLPBQbsFiKpUwLTUNI37AYk5gEbsUqIpJI&index=26&t=1324s 
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(generic.View):
    def post(self,*args,**kwargs):
        order = Order.objects.get(id=self.kwargs['order_id'])
        ordertotalamount = order.get_final_amount
        host = self.request.get_host()

        # https://stripe.com/docs/checkout/quickstart?lang=python
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    "price_data": {
                        # Stripe uses cents instead of dollars
                        "unit_amount": int(ordertotalamount) * 100 ,
                        "currency": "usd",
                        "product_data": {
                            "name": order.id,
                            "description": 'Payment for Coffee Shop - order number '+'#'+ str(order.id)
                            #"images": [
                            #    f"{settings.BACKEND_DOMAIN}/{order.product.thumbnail}"
                            #],
                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={"product_id": order.id},
            mode='payment',
        
            success_url = "http://{}{}".format(host,reverse('ecommerce:payment-success')),
            cancel_url  = "http://{}{}".format(host,reverse('ecommerce:payment-cancel')), 
        )
        return redirect(checkout_session.url, code=303)


def payment_success(request):
    context = {
       'payment_status' :'payment',   
    }    
    return render(request,'ecommerce/payment_confirmation.html', context)


def payment_cancel(request):
    context = {
       'payment_status' :'unpayment',   
    }    
    return render(request,'ecommerce/payment_confirmation.html', context)


# flow these steps in these tutorials:
# https://www.youtube.com/watch?v=66joNBEyNwE
#  -https://stripe.com/docs/checkout/quickstart
# 0-https://stripe.com/docs/payments/checkout/fulfill-orders
# 1- https://stripe.com/docs/payments/checkout/fulfill-orders#install-stripe-cli
# 2- https://stripe.com/docs/payments/checkout/fulfill-orders#create-event-handler
# 3- https://stripe.com/docs/payments/checkout/fulfill-orders#testing-webhooks
# To test in command line i use this url:
#  stripe listen --forward-to localhost:8000/ecommerce/stripe/my_webhook/
# this only for test , then change with the next codes (step4...).
# @csrf_exempt
# def my_webhook_view(request):
#   stripe.api_key = settings.STRIPE_SECRET_KEY
#   payload = request.body
#   # For now, you only need to print out the webhook payload so you can see
#   # the structure.
#   print(payload)
#   return HttpResponse(status=200)

# 4 -https://stripe.com/docs/payments/checkout/fulfill-orders#verify-events-came-from-stripe
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = settings.STRIPE_SECRET_KEY

# You can find your endpoint's secret in your webhook settings
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print(event['type'])
        session = event['data']['object']
        print('session='+ str(session))
        # Check if the order is already paid (for example, from a card payment)
        # A delayed notification payment will have an `unpaid` status, as
        # you're still waiting for funds to be transferred from the customer's
        # account.
        if session.payment_status == "paid": 
            print('session.payment_status == paid')

            # Fulfill the purchase
            line_item = session.list_line_items(session.id,limit=1).data[0]
            print('line_item='+ str(line_item))
            order_id = line_item['description']
            print('order_id='+str(line_item['description']))
            fulfill_order(order_id) # stripe run function to deal with orde model object
            print('fulfill done :)')
    # Passed signature verification
    return HttpResponse(status=200)



def fulfill_order(order_id):
    order = Order.objects.get(id=order_id)
    order.finish = True
    order.order_date = datetime.datetime.now()
    order.save()

    #for item in order.orderproducts.all():
   
        

















# @csrf_exempt
# def create_checkout_session(request):
#     if request.method == 'GET':
#         domain_url = 'http://localhost:8000/'
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         try:
#             # Create new Checkout Session for the order
#             # Other optional params include:
#             # [billing_address_collection] - to display billing address details on the page
#             # [customer] - if you have an existing Stripe Customer ID
#             # [payment_intent_data] - capture the payment later
#             # [customer_email] - prefill the email input in the form
#             # For full details see https://stripe.com/docs/api/checkout/sessions/create

#             # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
#             checkout_session = stripe.checkout.Session.create(
#                 success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
#                 cancel_url=domain_url + 'cancelled/',
#                 payment_method_types=['card'],
#                 mode='payment',
#                 line_items=[
#                    {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                   # 'price': '{{PRICE_ID}}',
                  #  'quantity': 1,
               # },
#                 ]
#             )
#             return JsonResponse({'sessionId': checkout_session['id']})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})




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