from rest_framework.response import Response
from rest_framework import status
from management_app.serializer.BrandSerializer import *
from ..models import *
# from sales_client_app.paginations import WebProductPaginationClass
from django.utils.text import slugify
from rest_framework.views import APIView
from django.db.models import Q



class BrandAPI(APIView):

    def get(self,request):
        brands = BrandModel.objects.all()
        serializer = BrandSerializer(brands,many=True)
        return Response({'status':True,'data':serializer.data,'message':'Brands Successfully retreived'})
    
    def post(self,request):
        data = request.data
        serializer = BrandSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':'Brand Successfully added'})
        
        return Response({'status':False,'errors':serializer.errors})
    
    def patch(self,request,id):
        try:
            brand = BrandModel.objects.get(id=id)
            serializer = BrandSerializer(brand,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'data':serializer.data,'message':'Brand Successfully updated'})
            return Response({'status':False,'errors':serializer.errors})
        except BrandModel.DoesNotExist:
            return Response({'status':False,'message':'Brand not available'})
    

    def delete(self,request,id):
        try:
            brand = BrandModel.objects.get(id=id)
            brand.delete()
            return Response({'status':True,'message':'Brand Successfully deleted'})

        except BrandModel.DoesNotExist:
           return Response({'status':False,'message':'Brand not available'})
           