from django.urls import path
from . import views

app_name = 'ecommerce'
urlpatterns = [
    path('add_to_cart/<int:pro_id>/',views.add_to_cart, name='add-to-cart'),
    path('cart_view/<str:order_id>',views.cart_view, name='cart-view'),
    path('increase_quent/<str:order_id>/<str:item_id>/',views.increase_quality, name='increase-quent'),
    path('decrease_quent/<str:order_id>/<str:item_id>/',views.decrease_quality, name='decrease-quent'),
    path('delete_item/<str:order_id>/<str:item_id>/',views.delete_orderproduct, name='delete-item'),
   
    path('checkout_view/<str:order_id>/',views.checkout_view, name='checkout-view'),
    path('editaddress_view/<str:order_id>/',views.editaddress_view, name='editaddress-view'),
    path('paymentmode/<str:order_id>/',views.add_payment_mode, name='add_payment_mode'),

    # stripe
    # https://stripe.com/docs/checkout/quickstart?lang=python
    path('stripe/create_checkout_session/<str:order_id>/',views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('stripe/payment_success/',views.payment_success, name='payment-success'),
    path('stripe/payment_cancel/',views.payment_cancel, name='payment-cancel'),
    path('stripe/my_webhook/', views.my_webhook_view, name='my_webhook')
    
    # path('update_cart/<int:pro_id>/',views.update_cart_form_view, name='update-cart-form-view'),
]