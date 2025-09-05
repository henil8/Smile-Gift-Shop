from django.urls import path,include
from management_app.View.CategoryAPI import *
from management_app.View.ProductAPI import *
from management_app.View.BrandAPI import *
from management_app.MobileAPIView.ProductViews import GetProductAPI, FilterProductAPI, AddProductAPI
from management_app.MobileAPIView.FavouriteViews import AddFavouriteAPI, RemoveFavouriteAPI, ListFavouriteAPI


urlpatterns = [

    path('categories/',CategoryAPI.as_view(),name='categories'),
    path('categories/<int:id>/',CategoryAPI.as_view(),name='categories'),

    path('sub-categories/',SubCategoryAPI.as_view(),name='sub-categories'),
    path('sub-categories/<int:id>/',SubCategoryAPI.as_view(),name='sub-categories'),

    path('products/',ProductAPI.as_view(),name='products'),
    path('products/<int:id>/',ProductAPI.as_view(),name='products'),

    path('brands/',BrandAPI.as_view(),name='brands'),
    path('brands/<int:id>/',BrandAPI.as_view(),name='brands'),


    path('get_product/', GetProductAPI.as_view(), name='getproduct-api'),
    path('filter_product/', FilterProductAPI.as_view(), name='filterproduct-api'),
    path('add_product/', AddProductAPI.as_view(), name='addproduct-api'),

    path('add_favourite/', AddFavouriteAPI.as_view(), name='add-favourite'),
    path('remove_favourite/', RemoveFavouriteAPI.as_view(), name='remove-favourite'),
    path('list_favourite/', ListFavouriteAPI.as_view(), name='list-favourite')
]