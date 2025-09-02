from django.urls import path,include
from management_app.View.CategoryAPI import *
from management_app.View.ProductAPI import *
from management_app.MobileAPIView.CartAPIView import GetCartAPIView
from management_app.View.BrandAPI import *
from management_app.View.CategoryAPIView import *

urlpatterns = [

    path('categories/',CategoryAPI.as_view(),name='categories'),
    path('categories/<int:id>/',CategoryAPI.as_view(),name='categories'),

    path('sub-categories/',SubCategoryAPI.as_view(),name='sub-categories'),
    path('sub-categories/<int:id>/',SubCategoryAPI.as_view(),name='sub-categories'),

    path('products/',ProductAPI.as_view(),name='products'),
    #mobile api
    path('mobile/cart-list/', GetCartAPIView.as_view(), name='cart-list')

    path('products/<int:id>/',ProductAPI.as_view(),name='products'),

    path('brands/',BrandAPI.as_view(),name='brands'),
    path('brands/<int:id>/',BrandAPI.as_view(),name='brands'),
    
    path('category/',CategoryList.as_view(),name='category'),
    path('sub-category/',SubCategoryList.as_view(),name='category'),

]