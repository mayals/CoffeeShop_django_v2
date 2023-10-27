from django.urls import path
from . import views


app_name = 'pages'
urlpatterns = [
    path('index/',views.index_view, name='index'),
    path('about/',views.about_view, name='about'),
    path('coffee/',views.coffee_view, name='coffee'),
    path('contact_us/',views.ContactUsView.as_view(), name='contact-us'),
    # for admin only
    path('dashboard/',views.dashboard_view, name='dashboard'),
    path('all_users/', views.all_users, name="all-users"),
]