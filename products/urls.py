from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('add_new_product/',views.create_product_form_view, name='add-new-product'),
    path('products/',views.products_view, name='products'),
    path('product/<int:pro_id>/', views.ProductDetailView.as_view(), name='product'),
    # path('product/<int:pro_id>/',views.product_view, name='product'),
    path('update_product/<int:pro_id>/',views.update_product_view, name='update-product'),
    path('delete_product/<int:pro_id>/',views.delete_product_view, name='delete-product'),
    path('like_product/<int:pro_id>/',views.create_product_like, name='like-product'),
    path('user_favorites/<str:user_id>/',views.user_favorites, name='user-favorites'),
    path('review_rating_product/<int:pro_id>/',views.review_rating_product, name='review_rating_product'),
    path('search/',views.search_view, name='search'),
  
]