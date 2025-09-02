from django.urls import path,include
from user_app.View.SignInAPI import SignInView,LogoutView
from user_app.View.ChangePasswordAPI import ChangePasswordView

#mobile api
from user_app.MobileAPIView.LoginViewAPI import LoginView
from user_app.MobileAPIView.SignUpView import SignUpView
from user_app.MobileAPIView.VerifyOTPViewAPI import VerifyOtpAPIView
from user_app.MobileAPIView.AddressViewAPI import AddressListView, AddressCreateView
from user_app.MobileAPIView.UserManagementView import UserUpdateView, UserDeleteView, GetUserView


urlpatterns = [
    
    path('signin/',SignInView.as_view(),name='sign-in'),
    path('change-password/',ChangePasswordView.as_view(),name='change-password'),
    path('logout/',LogoutView.as_view(),name='logout'),
    
    #mobile api
    path('mobile/login/', LoginView.as_view() , name='login' ),
    path('mobile/signup/',SignUpView.as_view(),name='signup'),
    path("mobile/verify-otp/", VerifyOtpAPIView.as_view(), name="verify-otp"),
    path("mobile/address/list/", AddressListView.as_view(), name="address-list"),
    path("mobile/address/add/", AddressCreateView.as_view(), name="add-address"),
    path('mobile/update-profile/',UserUpdateView.as_view(),name='user-update'),
    path('mobile/delete-account/',UserDeleteView.as_view(), name='delete-account'),
    path('mobile/get-user-profile/', GetUserView.as_view(), name="user-detail"),
]