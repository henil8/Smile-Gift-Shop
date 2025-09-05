from django.db.models import Q
from django.http import Http404, HttpResponse
from django.utils.text import slugify
from ..models import *
import requests
import json 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import filters,generics
from management_app.serializer.CategorySerializer import *
from django.conf import settings

class CategoryList(APIView):
    def post(self,request):
        # queryset= CategoryModel.objects.all()
        queryset = CategoryModel.get_root_nodes().filter(is_active=True).order_by('id')
        serialized=CategorySerializer(queryset,many=True)
        
        data = {
            "status":True,
            "message":"List Category Successfully",
            "data": serialized.data,
            "base_url": "http://192.168.1.15:5000"
        }
        return Response(data)
    
class SubCategoryList(APIView):
    def post(self, request):
        category_id = request.data.get("category_id")
        if not category_id:
            return Response({
                "status": False,
                "message": "category_id is required"
            }, status=status.HTTP_200_OK)

        try:
            parent = CategoryModel.get_root_nodes().filter(is_active=True).order_by("id").get(id=category_id)
            
            subcategories = parent.get_children() 
            
            serializer = SubCategorySerializer(subcategories, many=True)

            return Response({
                "status": True,
                "message": "List Category Successfully",
                "data": serializer.data,
                "base_url": "http://192.168.1.15:5000"
            }, status=status.HTTP_200_OK)
            
        except CategoryModel.DoesNotExist:
            return Response({
                "status": False,
                "message": "Data not found",
                "errors": "Data Not Found"
            }, status=status.HTTP_200_OK)

        
