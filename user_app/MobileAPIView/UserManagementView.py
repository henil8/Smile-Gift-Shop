from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import UserModel
from ..serializers import UserSerializer
from rest_framework.authtoken.models import Token

class GetUserView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response(
                {"status":False, "message": "user_id is required"},
                status = status.HTTP_200_OK,
            )
        
        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "User Not Found",
                    "errors": "User Not Found",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        serializer = UserSerializer(user)

        return Response({
            "status": True,
            "message": "List User Profile Successfully",
            "data": [serializer.data],
            "base_url": "http://192.168.1.15:5000"
        })
    
class UserUpdateView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {"status": False, "message": "user_id is required"},
                status=status.HTTP_200_OK,
            )

        user = get_object_or_404(UserModel, id=user_id)

        data = request.data.copy()
        if "mobile_no" in data:
            data.pop("mobile_no")

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Profile updated successfully",
                    "data": serializer.data,
                    "base_url": "http://192.168.1.15:5000"
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": False, "errors": serializer.errors},
            status=status.HTTP_200_OK,
        )
    
class UserDeleteView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {"status": False, "message": "user_id is required"},
                status=status.HTTP_200_OK,
            )

        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "User with this ID was not found",
                    "errors": "User Not Found",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # delete DRF Token if exists
        Token.objects.filter(user=user).delete()

        user.delete()
        return Response(
            {"status": True, "message": "Account deleted successfully"},
            status=status.HTTP_200_OK,
        )