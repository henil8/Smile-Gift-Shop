from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from management_app.serializer.FavouriteSerializer import FavouriteSerializer, ProductSerializer
from management_app.models import FavouriteModel, ProductModel
from django.utils import timezone

class AddFavouriteAPI(APIView):
    def post(self, request):

        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')

        record = FavouriteModel.objects.filter(user_id=user_id, product_id=product_id).first()
        if record:
            record.deleted_at = None
            record.save()
            return Response({'status':True, 'message':'Added to favourites successfully'}, status=status.HTTP_200_OK)

        serializer = FavouriteSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True, 'data':serializer.data, 'message':'Added to favourites successfully'}, status=status.HTTP_200_OK)
        return Response({'status':False, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class RemoveFavouriteAPI(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')

        favouriteFilter = FavouriteModel.objects.filter(user_id=user_id, product_id=product_id)
        if favouriteFilter.exists():
            favouriteFilter.update(deleted_at=timezone.now())
            return Response({'status':True, 'message':'Removed from favourites successfully'}) 
        return Response({'status':False, 'message':'Favourite not found'}, status=status.HTTP_400_BAD_REQUEST)
    

class ListFavouriteAPI(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        from_price = request.data.get('from_price')
        to_price = request.data.get('to_price')
        sort_by = request.data.get('sort_by')
    
        favourite_product = FavouriteModel.objects.filter(user_id=user_id).values_list('product_id', flat=True).exclude(deleted_at__isnull=False)

        products = ProductModel.objects.filter(id__in=favourite_product)

        if from_price and to_price: 
            products = products.filter(product_price__gte=from_price, product_price__lte=to_price)

        if sort_by == "high":

            products = products.order_by("-product_price")
        else:
            products = products.order_by("product_price")

        serializer = ProductSerializer(products, many=True, context={'request': request})

        return Response({'status': True,'message': 'Favourites listed successfully','data': serializer.data, 'base_url':'http://192.168.1.15:5000'}, status=status.HTTP_200_OK)
