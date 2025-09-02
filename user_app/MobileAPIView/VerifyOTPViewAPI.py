import datetime
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from ..models import ProfileModel
from ..serializers import UserSerializer


class VerifyOtpAPIView(APIView):
    def post(self, request):
        mobile_no = request.data.get("mobile_no")
        user_id = request.data.get("user_id")
        otp = request.data.get("otp")

        if not otp:
            return Response(
                {"status": False, "message": "OTP is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not mobile_no and not user_id:
            return Response(
                {"status": False, "message": "Either user_id or mobile_no is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if user_id:  
                profile = ProfileModel.objects.get(user__id=user_id)
            else:      
                profile = ProfileModel.objects.get(user__mobile_no=mobile_no)
        except ProfileModel.DoesNotExist:
            return Response(
                {"status": False, "message": "User profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # OTP match check
        if str(profile.otp) != str(otp):
            return Response(
                {
                    "status": False,
                    "message": "Validation error",
                    "errors": "Invalid OTP",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # OTP verified → clear otp
        profile.otp = None
        profile.save()

        user = profile.user
        token, created = Token.objects.get_or_create(user=user)   # generate token
        user_data = UserSerializer(user).data

        return Response(
            {
                "status": True,
                "message": "OTP verified successfully.",
                "token": token.key,
                "data": user_data,
            },
            status=status.HTTP_200_OK,
        )
