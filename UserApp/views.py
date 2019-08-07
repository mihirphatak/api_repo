import uuid
import time
from django.contrib.auth import authenticate
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.views import APIView
from app.settings import SECRET_KEY
from UserApp.models import User
from UserApp.serializers import UserProfileSerializer
from UtilityApp.views import UtilityMethods, DataValidationError
from collections import defaultdict


# Create your views here.
#Login
class Login(APIView):
    def post(self, request):
        status, response_data = UtilityMethods.get_default_response()
        u_fields = User.FieldNames
        required_fields = [u_fields.contact_number, u_fields.password]
        try:
            received_data = UtilityMethods.get_required_data(required_fields, request.data)
            user=User.objects.filter(contact_number=received_data[u_fields.contact_number],password=received_data[u_fields.password])
            data=defaultdict(str)
            if user.exists():
                data = {
                UtilityMethods.SUCCESS_KEY: True,
                'user_id': user[0].id,
                'user_type': user[0].user_type,
                'contact_number': user[0].contact_number,
                
            }
            else:
                raise User.DoesNotExist()
        except User.DoesNotExist:
            data = {
                UtilityMethods.ERROR_KEY: 'Wrong Contact/Password'
            }
        except DataValidationError as e:
            data = {
                UtilityMethods.ERROR_KEY: e.args[1]
            }
        return Response(data=data, status=status)


#UserProfile
class UserProfile(APIView):
    def post(self, request):
        status, response_data = UtilityMethods.get_default_response()
        u_fields = User.FieldNames
        required_fields = [u_fields.contact_number]
        try:
            received_data = UtilityMethods.get_required_data(required_fields, request.data)
            user=User.objects.filter(contact_number=received_data[u_fields.contact_number])
            if user.exists():
                data = {
                UtilityMethods.SUCCESS_KEY: True,
                'user_type': user[0].user_type,
                'contact_number': user[0].contact_number,
                'first_name': user[0].first_name,
                'last_name': user[0].last_name,
                'email': user[0].email
            }
            else:
                raise User.DoesNotExist()
        except User.DoesNotExist:
            data = {
                UtilityMethods.ERROR_KEY: 'Wrong Contact/Password'
            }
        except DataValidationError as e:
            data = {
                UtilityMethods.ERROR_KEY: e.args[1]
            }
        return Response(data=data, status=status)

#Registrationn
class Register(APIView):
    def put(self, request):
        status, response_data = UtilityMethods.get_default_response()
        u_fields = User.FieldNames
        required_fields = [u_fields.user_type,u_fields.contact_number,u_fields.first_name,u_fields.last_name,
            u_fields.email, u_fields.password]
        
        received_data = UtilityMethods.get_required_data(required_fields, request.data)
        user=User.objects.filter(contact_number=received_data[u_fields.contact_number])
        if user.exists():
            data = {
            UtilityMethods.SUCCESS_KEY: False,
            UtilityMethods.ERROR_KEY: 'User Exists'
        }
        else:
            ut = received_data[u_fields.user_type]
            cno = received_data[u_fields.contact_number]
            fname = received_data[u_fields.first_name]
            lname = received_data[u_fields.last_name]
            email1 = received_data[u_fields.email]
            passw  =received_data[u_fields.password]
            print(received_data)
            user = User.objects.create(user_type=ut,contact_number = cno,
                    first_name =fname,
                    last_name = lname,
                    email = email1,
                    password = passw)
            data = {UtilityMethods.SUCCESS_KEY: True}          
        return Response(data=data, status=status)

#Edit Profile
class EditProfile(APIView):
    def post(self, request):
        status, response_data = UtilityMethods.get_default_response()
        u_fields = User.FieldNames
        required_fields = [u_fields.contact_number,u_fields.first_name,u_fields.last_name,u_fields.email]
        try:
            received_data = UtilityMethods.get_required_data(required_fields, request.data)
            user=User.objects.filter(contact_number=received_data[u_fields.contact_number])
            if user.exists():
                cno = received_data[u_fields.contact_number]
                fname = received_data[u_fields.first_name]
                lname = received_data[u_fields.last_name]
                email1 = received_data[u_fields.email]
                user1 = User.objects.filter(contact_number=received_data[u_fields.contact_number]).update(first_name =fname,last_name = lname,
                     email = email1)
                data = {
                    UtilityMethods.SUCCESS_KEY: True,
                }
            else:
                raise User.DoesNotExist()
        except User.DoesNotExist:
            data = {
                 UtilityMethods.ERROR_KEY: 'Wrong Contact/Password'
            }
        except DataValidationError as e:
            data = {
                UtilityMethods.ERROR_KEY: e.args[1]
            }
        return Response(data=data, status=status)

