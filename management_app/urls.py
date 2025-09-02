from django.urls import path,include
from management_app.View.CategoryAPI import *
from management_app.View.ProductAPI import *

from management_app.MobileAPIView.CartAPIView import GetCartAPIView

urlpatterns = [

    path('categories/',CategoryAPI.as_view(),name='categories'),
    path('categories/<int:id>/',CategoryAPI.as_view(),name='categories'),
    path('sub-categories/',SubCategoryAPI.as_view(),name='sub-categories'),
    path('sub-categories/<int:id>/',SubCategoryAPI.as_view(),name='sub-categories'),
    path('products/',ProductAPI.as_view(),name='products'),

    #mobile api
    path('mobile/cart-list/', GetCartAPIView.as_view(), name='cart-list')
]