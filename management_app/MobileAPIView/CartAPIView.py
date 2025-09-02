from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..models import Cart, UserModel, ProductModel, BrandModel
from management_app.serializer.CartSerializer import CartSerializer


class GetCartAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({
                "status": False,
                "message": "User ID is required",
                "errors": {"user_id": "This field is required"}
            }, status=status.HTTP_400_BAD_REQUEST)

        user = UserModel.objects.filter(id=user_id).first()
        if not user:
            return Response({
                "status": False,
                "message": "User Not Found",
                "errors": "User Not Found"
            }, status=status.HTTP_404_NOT_FOUND)

        carts = Cart.objects.filter(user=user, status=0)

        if not carts.exists():
            return Response({
                "status": False,
                "message": "Your cart is empty",
                "errors": "Data not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(carts, many=True)

        return Response({
            "status": True,
            "message": "Cart fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class AddToCartAPIView(APIView):
    """
    POST request with {"user_id": 1, "product_id": 2, "qty": 3}
    to add a product into user's cart
    """
    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        product_id = request.data.get("product_id")
        qty = request.data.get("qty", 1)

        # User check
        user = UserModel.objects.filter(id=user_id).first()
        if not user:
            return Response({
                "status": False,
                "message": "User Not Found",
                "errors": "User Not Found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Product check
        product = ProductModel.objects.filter(id=product_id).first()
        if not product:
            return Response({
                "status": False,
                "message": "Product Not Found",
                "errors": "Product Not Found"
            }, status=status.HTTP_404_NOT_FOUND)

        # If cart item already exists → update qty
        cart_item, created = Cart.objects.get_or_create(
            user=user,
            product=product,
            defaults={"qty": qty, "price": product.product_price}
        )
        if not created:
            cart_item.qty += int(qty)
            cart_item.save()

        serializer = CartSerializer(cart_item)

        return Response({
            "status": True,
            "message": "Item added to cart successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
