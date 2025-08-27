from rest_framework.response import Response
from rest_framework import status
from management_app.serializer.CategorySerializer import *
from ..models import *
# from sales_client_app.paginations import WebProductPaginationClass
from django.utils.text import slugify
from rest_framework.views import APIView
from django.db.models import Q


class CategoryAPI(APIView):
    def get(self,request):
        categories = CategoryModel.objects.filter(is_active=True).order_by('id')
        category_list=[]
        for category in categories:
            if category.is_root():
                categories = CategorySerializer(category).data
                category_list.append(categories)
            else:
                continue
        
        return Response({'status':True,'Categories':category_list,'message':'Categories successfully displayed'})
    
    def post(self,request):
        data = request.data
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({'status':True,'data':serializer.data,'message':'Category successfully added'})
        else:
             return Response({'status':False,'errors':serializer.errors})
        
    def patch(self,request,id):
        try:
            category = CategoryModel.objects.get(id=id)
            serializer = CategorySerializer(category,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'data':serializer.data,'message':'Category successfully updated'})
            else:
                return Response({'status':False,'errors':serializer.errors})
        except CategoryModel.DoesNotExist:
            return Response({'status':False,'message':'Category not available'})
        
    def delete(self,request,id):
        try :
            category = CategoryModel.objects.get(id=id)
            category.delete()
            return Response({'status':True,'message':'Category successfully deleted'})
        except CategoryModel.DoesNotExist:
           return Response({'status':True,'message':'Category not available'})
                 

            
class SubCategoryAPI(APIView):
    def get(self,request):
        sub_categories = CategoryModel.objects.filter(is_active=True).order_by('id')
        sub_categories_list=[]
        for sub_category in sub_categories:
            if sub_category.get_parent():
                sub_categories = SubCategorySerializer(sub_category).data
                sub_categories_list.append(sub_categories)
            else:
                continue
        
        return Response({'status':True,'Sub Categories':sub_categories_list,'message':'Categories successfully displayed'})
    
    def post(self,request):
        data = request.data
        serializer = SubCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':'Sub Category successfully added'})
        else:
             return Response({'status':False,'errors':serializer.errors})
        
    def patch(self,request,id):
        try:
              
           sub_category = CategoryModel.objects.get(id=id)
           serializer = SubCategorySerializer(sub_category,data=request.data,partial=True)
           if serializer.is_valid():
               serializer.save()
               return Response({'status':True,'data':serializer.data,'message':'Sub Category successfully updated'})
           else:
                return Response({'status':False,'errors':serializer.errors})
           
             
        except CategoryModel.DoesNotExist:
            return Response({'status':True,'message':'Sub Category not available'})
        
    def delete(self,request,id):
        try :
            sub_category = CategoryModel.objects.get(id=id)
            sub_category.delete()
            return Response({'status':True,'message':'Category successfully deleted'})
        except CategoryModel.DoesNotExist:
           return Response({'status':True,'message':'Category not available'})
