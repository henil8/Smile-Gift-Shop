from django.urls import path,include
from management_app.View.CategoryAPI import *
from management_app.View.ProductAPI import *
from management_app.View.BrandAPI import *

from management_app.MobileAPIView.CartAPIView import GetCartAPIView,AddToCartAPIView,UpdateCartAPIView,RemoveCartAPIView
from management_app.MobileAPIView.CategoryAPIView import *
from management_app.MobileAPIView.InquiryAPIView import *
from management_app.MobileAPIView.VersionCheckAPIView import *
from management_app.MobileAPIView.HomeAPIView import *
from management_app.MobileAPIView.FavouriteViews import AddFavouriteAPI, RemoveFavouriteAPI, ListFavouriteAPI
from management_app.MobileAPIView.ProductViews import GetProductAPI, FilterProductAPI, AddProductAPI, SubCategoryProductListAPI
# from management_app.MobileAPIView.OrderAPIView import PlaceOrderView, UserOrdersView, OrderDetailView


urlpatterns = [

    path('categories/',CategoryAPI.as_view(),name='categories'),
    path('categories/<int:id>/',CategoryAPI.as_view(),name='categories'),

    path('sub-categories/',SubCategoryAPI.as_view(),name='sub-categories'),
    path('sub-categories/<int:id>/',SubCategoryAPI.as_view(),name='sub-categories'),

    path('products/',ProductAPI.as_view(),name='products'),
    path('products/<int:id>/',ProductAPI.as_view(),name='products'),
    path('brands/',BrandAPI.as_view(),name='brands'),
    path('brands/<int:id>/',BrandAPI.as_view(),name='brands'),

  
    #mobile api
    path('mobile/list-product/', SubCategoryProductListAPI.as_view(), name='subcategoryproduct-api'),
    path('mobile/list-product-detail/', GetProductAPI.as_view(), name='getproduct-api'),
    path('mobile/all_brand_product_filter/', FilterProductAPI.as_view(), name='filterproduct-api'),
    path('mobile/add-product/', AddProductAPI.as_view(), name='addproduct-api'),

    path('mobile/category/',CategoryList.as_view(),name='category'),
    path('mobile/sub-category/',SubCategoryList.as_view(),name='category'),
    
    path('mobile/cart-list/', GetCartAPIView.as_view(), name='cart-list'),
    path('mobile/add-to-cart/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('mobile/update-cart/', UpdateCartAPIView.as_view(), name='update-cart'),
    path('mobile/remove-cart/', RemoveCartAPIView.as_view(), name='remove-cart'),
  
    path('mobile/add_favourite/', AddFavouriteAPI.as_view(), name='add-favourite'),
    path('mobile/remove_favourite/', RemoveFavouriteAPI.as_view(), name='remove-favourite'),
    path('mobile/list_favourite/', ListFavouriteAPI.as_view(), name='list-favourite'),
    path('mobile/add_product/', AddProductAPI.as_view(), name='addproduct-api'),
    
    # path('mobile/add-place-order/', PlaceOrderView.as_view(), name='place-order'),
    # path('mobile/list-product-order/', UserOrdersView.as_view(), name='user-orders'),
    # path('mobile/details-product-order/', OrderDetailView.as_view(), name='order-detail'),
  
    path('mobile/inquiry/',InquiryList.as_view(),name='category'),

    path('mobile/version-check/',VersionList.as_view(),name='category'),
    path('mobile/home/',HomeList.as_view(),name='home'),


    
]