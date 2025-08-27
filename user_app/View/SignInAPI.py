from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied
from user_app.models import *
from uuid import uuid4
from django.core.mail import send_mail
from copy import deepcopy
from secrets import token_urlsafe
from dateutil.relativedelta import relativedelta
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.decorators import renderer_classes
from django.utils import timezone
from django.db.models import Q
import random
import string
from user_app.models import UserModel
from collections import defaultdict

class SignInView(APIView):
    def post(self, request, format=None):
        try:
            email = request.data['email']
            password = request.data['password']
           
            if UserModel.objects.get(email=email).is_active == True:
                auth_user = authenticate(username=email, password=password)
                if auth_user is not None:
                        data = dict()
                        obj, _ = Token.objects.get_or_create(user=auth_user)
                        login(request, auth_user)

                        
                        

                        data['id'] = auth_user.id
                        data['first_name'] = auth_user.first_name
                        data['last_name'] = auth_user.last_name
                        data['email'] = auth_user.email
                        data['token'] = obj.key
                        
                        
                        return Response({'status': True, 'data': data, 'message': 'User successfully logged in'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': False, 'message': 'Invalid credentials!'}, status=status.HTTP_400_BAD_REQUEST)
                   
            else:
                return Response({'status': False, 'message': 'Your account has been deactivated!'}, status=status.HTTP_400_BAD_REQUEST)
        except UserModel.DoesNotExist:
            return Response({'status': False, 'message': 'Invalid credentials!'}, status=status.HTTP_400_BAD_REQUEST)
  

class LogoutView(APIView):
    def post(self, request, format=None):
        if request.user.is_authenticated:
            logout(request)
            return Response({'status': True, 'message': 'User successfully logged out'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'message': 'Login is required'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)