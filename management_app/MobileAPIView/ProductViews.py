from management_app.models import ProductModel
from rest_framework.views import APIView
from management_app.serializer.ProductSerializer import ProductListSerializer, ProductSerializer , MobileProductSerializer
from rest_framework.response import Response
from rest_framework import status

class GetProductAPI(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        products = ProductModel.objects.all()

        if product_id:
            products = products.filter(id=product_id)
            serializer = MobileProductSerializer(products, many=True)
            return Response({'status':True, 'data':serializer.data, 
                             'mesage':'Product Detail Show Successfully',
                             "base_url_document": "http://192.168.1.15:5000",
                            "base_url_product": "http://192.168.1.15:5000",
                            "base_url_subcategory": "http://192.168.1.15:5000",
                            "base_url_category": "http://192.168.1.15:5000"
                             }, status=status.HTTP_200_OK)
        return Response({'status': False, 'error': 'Product ID is required'},status=status.HTTP_200_OK)

class FilterProductAPI(APIView):
    def post(self, request):
        category_id = request.data.get('category_id')  
        from_price = request.data.get('from_price') 
        to_price = request.data.get('to_price')
        sort_by = request.data.get('sort_by')
 
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


        serializer = MobileProductSerializer(productes, many=True)
        return Response(
            {'status':True, 
             'message':'List Product Successfully',
             "brand_banner":" ", 'data':serializer.data,
             "base_url_document": "http://192.168.1.15:5000",
            "base_url_product": "http://192.168.1.15:5000",
            "base_url_subcategory": "http://192.168.1.15:5000",
            "base_url_category": "http://192.168.1.15:5000"
             }, status=status.HTTP_200_OK)


class AddProductAPI(APIView):    
    def post(self, request):
        products = request.data.get('products', [])
        serializer = ProductSerializer(data=products, many=True, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True, 'remark':'null', 'data':serializer.data, 'message':'Your Order Added Successfully'}, status=status.HTTP_200_OK)
        return Response({'status':False, 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SubCategoryProductListAPI(APIView):
    def post(self, request):
        sub_category_id = request.data.get('sub_category_id')
        
        if not sub_category_id:
            products = ProductModel.objects.all()
        else:
            products = ProductModel.objects.filter(sub_category = sub_category_id)
            
        serializer = MobileProductSerializer(products, many=True)
        
        return Response({
            'status': True,
            'message': 'List Product Successfully',
            "brand_banner": "",
            'data': serializer.data,
            "base_url_document": "http://192.168.1.15:5000",
            "base_url_product": "http://192.168.1.15:5000",
            "base_url_subcategory": "http://192.168.1.15:5000",
            "base_url_category": "http://192.168.1.15:5000"
        })