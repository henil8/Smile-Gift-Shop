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

class CategoryList(APIView):
    def post(self,request):
        # queryset= CategoryModel.objects.all()
        queryset = CategoryModel.get_root_nodes().filter(is_active=True).order_by('id')
        serialized=CategorySerializer(queryset,many=True)
        data = {
            "status":True,
            "message":"List Category Successfully",
            "data": serialized.data
        }
        return Response(data)
    
class SubCategoryList(APIView):
    def post(self, request):
        category_id = request.data.get("category_id")
        if not category_id:
            return Response({
                "status": False,
                "message": "category_id is required",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            parent = CategoryModel.objects.get(id=category_id)
        except CategoryModel.DoesNotExist:
            return Response({
                "status": False,
                "message": "Parent category not found",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        subcategories = parent.get_children() 
        
        serializer = SubCategorySerializer(subcategories, many=True)

        return Response({
            "status": True,
            "message": "List Category Successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
