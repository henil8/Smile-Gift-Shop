from management_app.models import ProductModel
from rest_framework.views import APIView
from management_app.serializer.ProductSerializer import ProductListSerializer, ProductSerializer 
from rest_framework.response import Response
from rest_framework import status

class GetProductAPI(APIView):
    def post(self, request):
        product_id = request.query_params.get('product_id')
        products = ProductModel.objects.all()

        if product_id:
            products = products.filter(id=product_id)
            serializer = ProductListSerializer(products, many=True)
            return Response({'status':True, 'data':serializer.data, 'mesage':'List Category Successfully'}, status=status.HTTP_200_OK)
        return Response({'status': False, 'error': 'Product ID is required'},status=status.HTTP_400_BAD_REQUEST)

class FilterProductAPI(APIView):
    def post(self, request):
        category_id = request.query_params.get('category_id')  
        from_price = request.query_params.get('from_price') 
        to_price = request.query_params.get('to_price')
        sort_by = request.query_params.get('sort_by')
 
        productes = ProductModel.objects.all()

        if category_id:
            productes = productes.filter(category__in=category_id.split(','))

        if from_price and to_price:
            productes = productes.filter(product_price__gte=from_price, product_price__lte=to_price)

        if sort_by == "high":
            productes = productes.order_by("-product_price")
        elif sort_by == "low":
            productes = productes.order_by("product_price")
        elif sort_by == "a_to_z":
            productes = productes.order_by("name")
        elif sort_by == "z_to_a":
            productes = productes.order_by("-name")


        serializer = ProductListSerializer(productes, many=True)
        return Response({'status':True, 'message':'List Product Successfully', "brand_banner":" ", 'data':serializer.data}, status=status.HTTP_200_OK)


class AddProductAPI(APIView):    
    def post(self, request):
        products = request.data.get('products', [])
        serializer = ProductSerializer(data=products, many=True, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True, 'remark':'null', 'data':serializer.data, 'message':'Your Order Added Successfully'}, status=status.HTTP_200_OK)
        return Response({'status':False, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

