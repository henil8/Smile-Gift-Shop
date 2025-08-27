from django.urls import path,include
from user_app.View.SignInAPI import SignInView,LogoutView
from user_app.View.ChangePasswordAPI import ChangePasswordView


urlpatterns = [
    
    path('signin/',SignInView.as_view(),name='sign-in'),
    path('change-password/',ChangePasswordView.as_view(),name='change-password'),
    path('logout/',LogoutView.as_view(),name='logout')
    
]