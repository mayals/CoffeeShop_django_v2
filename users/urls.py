from django.urls import path
from users import views


app_name = 'users'
urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('signin/', views.signin_view, name="signin"),
    path('signout/', views.signout_view, name="signout"),
    path('profile/', views.profile_view, name="profile-view"),
    path('edit_profile/<str:prof_id>/', views.edit_profile_view, name="edit-profile"),
    # EmailConfirm
    path('confirm-email/<uidb64>/<str:token>/',views.confirmEmail_and_activateUser, name='confirmEmail_and_activateUser'),
]