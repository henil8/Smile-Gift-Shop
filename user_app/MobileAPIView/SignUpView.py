import random
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserSerializer
from ..models import ProfileModel


class SignUpView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        mobile_no = request.data.get('contact')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        firebase_token = request.data.get('firebase_token') 

        if not email or not mobile_no or not first_name or not last_name or not firebase_token:
            return Response(
                {'status': False, 'message': 'Email, Mobile no, First name, Last name and token are required'},
                status=status.HTTP_200_OK
            )
        
        if mobile_no and not mobile_no.startswith("+91"):
            mobile_no = f"+91{mobile_no}"

        try:
            if ProfileModel.objects.filter(mobile_no=mobile_no).exists():
                return Response(
                    {'status': False, 'message': f'Mobile number {mobile_no} already exists'},
                    status=status.HTTP_200_OK
                )
            
            request_data = request.data.copy()
            request_data['mobile_no'] = mobile_no

            serializer = UserSerializer(data=request_data)
            if serializer.is_valid():
                    user = serializer.save()

                    # Generate 6 digit OTP (not sent, only stored)
                    otp = random.randint(1000, 9999)

                    # Save ProfileModel with OTP
                    ProfileModel.objects.create(
                        user=user,
                        mobile_no=mobile_no,
                        otp=otp,
                        otp_requested_at=timezone.now()
                    )

                    user.refresh_from_db()   # ensures profile is loaded
                    response_serializer = UserSerializer(user)

                    return Response(
                        {
                            'status': True,
                            'message': 'User created successfully.',
                            'data': response_serializer.data
                        },
                        status=status.HTTP_201_CREATED
                    )
            else:
                return Response(
                    {'status': False, "message": f'User already exists with given email - {email}', 'errors': serializer.errors},
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            return Response({'error': "Something went wrong", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import Group
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from ..serializers import UserSerializer
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.conf import settings



# class SignUpView(APIView):

#     def post(self, request, format=None):
#         email = request.data.get('email')
#         mobile_no = request.data.get('mobile_no')
#         first_name = request.data.get('first_name', '')
#         last_name = request.data.get('last_name', '')
        
#         if not email or not mobile_no or not first_name or not last_name:
#             return Response({'status': False, 'message': 'Email, Mobile no, First name and Last name'}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             user_data = {}
#             serializer = UserSerializer(data=request.data)
#             if serializer.is_valid():
#                 if request.data['password'] == request.data['confirm_password']:
#                     user = serializer.save(
#                         password=make_password(request.data['password']))
#                     user_token = Token.objects.create(user=user)
#                     try:
#                         from_email = settings.EMAIL_HOST_USER
#                         to_email = [user.email]
#                         subject = "Welcome to Sweet Hamper!"
#                         html_content = render_to_string('welcome_register_mail.html',{'user_name':f'{user.first_name} {user.last_name}','shopping':'https://sweethamper.in/'})
            
#                         # Send email
#                         email = EmailMultiAlternatives(subject, html_content, from_email, to_email)
#                         email.attach_alternative(html_content, "text/html")
#                         email.send()
                                
#                     except Exception as e:
#                         pass

#                     return Response({'status': True, 'data': user_data, 'message': 'User successfully registered'}, status=status.HTTP_201_CREATED)
                    
#                 else:
#                     return Response({'status': False, 'message': 'Password does not match'}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 for i in serializer.errors:
#                     print(i, serializer.errors[i])
#                     return Response({'status': False, "message": f'User already exists with given email - {email} - {serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)
                
#         except Exception as e:
#             if str(e.args[0]) == 'password':
#                 return Response({'password': "This field is required."}, status=status.HTTP_400_BAD_REQUEST)
#             elif str(e.args[0]) == 'confirm_password':
#                 return Response({'confirm_password': "This field is required."}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'error': "Something went wrong", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

