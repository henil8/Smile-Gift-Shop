from rest_framework.response import Response
from rest_framework import status
from management_app.serializer.ProductSerializer import *
from ..models import *
# from sales_client_app.paginations import WebProductPaginationClass
from django.utils.text import slugify
from rest_framework.views import APIView
from django.db.models import Q



class ProductAPI(APIView):
    def get(self,request):
        products = ProductModel.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response({'status':True,'data':serializer.data,'message':'Products successfully retreived'},status=status.HTTP_200_OK)
    
    def post(self,request):
        data = request.data
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':'Products successfully added'},status=status.HTTP_200_OK)
        return Response({'status':True,'errors':serializer.errors},status=status.HTTP_200_OK)
    
    def patch(self,request):
        data=request.data