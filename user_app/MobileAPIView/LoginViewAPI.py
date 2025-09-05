import random
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import ProfileModel
from ..serializers import UserSerializer
from rest_framework.authtoken.models import Token

def generate_otp():
    return random.randint(1000, 9999) 


class LoginView(APIView):
    def post(self, request):
        mobile = request.data.get("contact")
        firebase_token = request.data.get("firebase_token")

        if not mobile:
            return Response(
                {"mobile": "This field is required."},
                status=status.HTTP_200_OK,
            )
        
        if not mobile.startswith("+91"):
                mobile = f"+91{mobile}"

        try:
            profile = ProfileModel.objects.get(mobile_no=mobile)
        except ProfileModel.DoesNotExist:
            return Response(
                {"status": False, "message": "Mobile number not registered!"},
                status=status.HTTP_200_OK,
            )

        # generate OTP
        otp_code = generate_otp()
        profile.otp = otp_code
        profile.otp_requested_at = timezone.now()
        profile.save()

        user = profile.user
        if firebase_token:
            user.token = firebase_token
            user.save(update_fields=["token"])

        profile.refresh_from_db()
        user_serializer = UserSerializer(user)
        token,_ = Token.objects.get_or_create(user=user)
        # TODO: send OTP via SMS/Email gateway here
        # send_sms(mobile, f"Your OTP is {otp_code}")

        return Response(
            {
                "status": True,
                "message": "otp sent successfully",
                "data" : user_serializer.data,
                "token" : "Token "+token.key
            },
            status=status.HTTP_200_OK,
        )





# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate, login
# from rest_framework.authtoken.models import Token

# from ..models import UserModel


# class LoginView(APIView):
#     def post(self, request, format=None):
#         try:
#             email = request.data.get("email")
#             password = request.data.get("password")

#             # fields validation
#             if not email:
#                 return Response({"email": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)
#             if not password:
#                 return Response({"password": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

#             # Check user exists
#             try:
#                 user_obj = UserModel.objects.get(email=email)
#             except UserModel.DoesNotExist:
#                 return Response(
#                     {"status": False, "message": "Please register to continue!"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # Check active status
#             if not user_obj.is_active:
#                 return Response(
#                     {"status": False, "message": "Your account has been deactivated!"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # Authenticate user
#             auth_user = authenticate(request=request, email=email, password=password)
#             if auth_user is None:
#                 return Response(
#                     {"status": False, "message": "Invalid credentials!"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # Create / Get token
#             token_obj, _ = Token.objects.get_or_create(user=auth_user)

#             # (Optional: log user into session as well)
#             login(request, auth_user)

#             # Response data
#             data = {
#                 "id": auth_user.id,
#                 "first_name": auth_user.first_name,
#                 "last_name": auth_user.last_name,
#                 "email": auth_user.email,
#                 "role": auth_user.role.name if auth_user.role else None,
#                 "is_staff": auth_user.is_staff,
#                 "is_superuser": auth_user.is_superuser,
#                 "groups": [g.name for g in auth_user.groups.all()],
#                 "token": token_obj.key,
#             }

#             return Response(
#                 {"status": True, "data": data, "message": "User successfully logged in"},
#                 status=status.HTTP_200_OK,
#             )

#         except Exception as e:
#             return Response(
#                 {"status": False, "message": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )
