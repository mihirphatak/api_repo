from django.shortcuts import render
import datetime
from django.utils import timezone
from django.db.models import Q
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.views import APIView
from BusinessPostApp.models import BusinessPost, BusinessCategory, BusinessPoints
from BusinessPostApp.serializers import BusinessPostSerializer, BusinessPostCategorySerializer, BusinessPostPointSerializer
from UtilityApp.views import UtilityMethods, DataValidationError
from BusinessPostApp.models import BusinessPost

class BusinessPostsListAPI(APIView):
    def post(self, request):
        status, response_data = UtilityMethods.get_default_response()
        required_fields = ["business_type"]
        #allowed_fields = ["search_query", "business_category_id", "business_type_code"]
        try:
            received_required_data = UtilityMethods.get_required_data(required_fields, request.data)
            # search_query = request.data.get("search_query", None)
            # business_category_id = request.data.get("business_category_id", None)
            # business_type_code = request.data.get("business_type_code", None)
            business_type = request.data.get("business_type", None)
            business_posts = BusinessPost.objects.all()
            
            if business_type == 'class':
                business_posts = BusinessPost.objects.filter(business_type = 'class')
            elif business_type == 'service':
                business_posts = BusinessPost.objects.filter(business_type = 'service')
            elif business_type == 'business':
                business_posts = BusinessPost.objects.filter(business_type = 'business')
            else:
                business_posts = BusinessPost.objects.all()
            
            


            serializer = BusinessPostSerializer(business_posts, many=True)
            
        except DataValidationError as e:
            response_data[UtilityMethods.MESSAGE_KEY] = {
                e.args[0]: e.args[1]
            }
            response_data[UtilityMethods.MESSAGE_KEY] = {
                UtilityMethods.ERROR_KEY: str(e)
            }
        except Exception as e:
            response_data[UtilityMethods.MESSAGE_KEY] = {
                UtilityMethods.ERROR_KEY: str(e)
            }
        return Response(data=serializer.data, status=status)


class CreateBusinessPostsAPI(APIView):
    def post(self, request):
        status, response_data = UtilityMethods.get_default_response()
        u_fields = BusinessPost.FieldNames
        required_fields = [u_fields.BUSINESS_TYPE,u_fields.BUSINESS_NAME_ENGLISH,u_fields.BUSINESS_CONTACT_NUMBER,
                u_fields.BUSINESS_POINT_1,u_fields.BUSINESS_POINT_2,u_fields.BUSINESS_POINT_3,u_fields.DISCOUNT,
                u_fields.EMAIL, u_fields.USER,u_fields.START_TIME,u_fields.END_TIME,u_fields.BUSINESS_ADDRESS,
                #u_fields.BUSINESS_IMAGE,u_fields.LIKES_COUNTER,u_fields.IS_PAYMENT_MADE,
                # u_fields.ARE_DETAILS_COMPLETE,u_fields.IS_ACTIVE
                u_fields.CITY,u_fields.BUSINESS_CATEGORY_ID]
        
        received_data = UtilityMethods.get_required_data(required_fields, request.data)
        user=BusinessPost.objects.filter(business_name_english=received_data[u_fields.BUSINESS_NAME_ENGLISH])
        if user.exists():
            data = {
            UtilityMethods.SUCCESS_KEY: False,
            UtilityMethods.ERROR_KEY: 'Business Name  Exists'
        }
        else:
            
            busi_post = BusinessPost.objects.create(
                    business_type = received_data[u_fields.BUSINESS_TYPE],
                    business_name_english = received_data[u_fields.BUSINESS_NAME_ENGLISH],
                    business_contact_number = received_data[u_fields.BUSINESS_CONTACT_NUMBER],
                    business_point_1 = received_data[u_fields.BUSINESS_POINT_1],
                    business_point_2 = received_data[u_fields.BUSINESS_POINT_2],
                    business_point_3 = received_data[u_fields.BUSINESS_POINT_3],
                    discount = received_data[u_fields.DISCOUNT],
                    email = received_data[u_fields.EMAIL],
                    start_time = received_data[u_fields.START_TIME],
                    end_time = received_data[u_fields.END_TIME],
                    business_address = received_data[u_fields.BUSINESS_ADDRESS],
                    #business_image = received_data[u_fields.BUSINESS_IMAGE],
                    #likes_counter = received_data[u_fields.LIKES_COUNTER],
                    city = received_data[u_fields.CITY],
                    is_payment_made = True,
                    are_details_complete = True,
                    is_active = True,
                    business_category_id = received_data[u_fields.BUSINESS_CATEGORY_ID],
                    user_id = received_data[u_fields.USER]
            )
         
                
            data = {UtilityMethods.SUCCESS_KEY: True}          
        return Response(data=data, status=status)


class BusinessPostsListUserAPI(APIView):
    def post(self, request):
        status, response_data = UtilityMethods.get_default_response()
        required_fields = ["user_id"]
        try:
            received_required_data = UtilityMethods.get_required_data(required_fields, request.data)
            user_id = request.data.get("user_id")
            business_posts = BusinessPost.objects.filter(user_id=user_id)
            serializer = BusinessPostSerializer(business_posts, many=True)
           
        except DataValidationError as e:
            response_data[UtilityMethods.MESSAGE_KEY] = {
                e.args[0]: e.args[1]
            }
            response_data[UtilityMethods.MESSAGE_KEY] = {
                UtilityMethods.ERROR_KEY: str(e)
            }
        except Exception as e:
            response_data[UtilityMethods.MESSAGE_KEY] = {
                UtilityMethods.ERROR_KEY: str(e)
            }
        return Response(data=serializer.data, status=status)


class EditBusinessPostsAPI(APIView):
    def post(self, request):
        status, response_data = UtilityMethods.get_default_response()
        b_fields = BusinessPost.FieldNames
        required_fields = [b_fields.ID,
                           b_fields.BUSINESS_CONTACT_NUMBER,
                           b_fields.BUSINESS_TYPE,
                           b_fields.BUSINESS_NAME_ENGLISH,
                           b_fields.BUSINESS_NAME_MARATHI,
                           b_fields.START_TIME,
                           b_fields.END_TIME,
                           b_fields.WEEKLY_OFF,
                           b_fields.BUSINESS_ADDRESS,
                           b_fields.EMAIL,
                           b_fields.BUSINESS_IMAGE,
                           b_fields.CITY,
                           b_fields.LATITUDE,
                           b_fields.LONGITUDE]
        try:
            received_data = UtilityMethods.get_required_data(required_fields, request.data)
            post_object=BusinessPost.objects.filter(id=received_data[b_fields.ID])
            if post_object.exists():
                contact = received_data[b_fields.BUSINESS_CONTACT_NUMBER]
                b_type = received_data[b_fields.BUSINESS_TYPE]
                name_eng = received_data[b_fields.BUSINESS_NAME_ENGLISH]
                name_mar = received_data[b_fields.BUSINESS_NAME_MARATHI]
                start = received_data[b_fields.START_TIME]
                end = received_data[b_fields.END_TIME]
                off = received_data[b_fields.WEEKLY_OFF]
                add = received_data[b_fields.BUSINESS_ADDRESS]
                eml = received_data[b_fields.EMAIL]
                image = received_data[b_fields.BUSINESS_IMAGE]
                bcity = received_data[b_fields.CITY]
                lat = received_data[b_fields.LATITUDE]
                long = received_data[b_fields.LONGITUDE]
                post_object2 = BusinessPost.objects.filter(id=received_data[b_fields.ID]).update(business_type = b_type,
                                                                                                 business_name_english = name_eng,
                                                                                                 business_contact_number = contact,
                                                                                                 start_time = start,
                                                                                                 end_time = end,
                                                                                                 weekly_off = off,
                                                                                                 business_address = add,
                                                                                                 email = eml,
                                                                                                 business_image = image,
                                                                                                 city = bcity,
                                                                                                 latitude = lat,
                                                                                                 longitude = long)
                data = {
                    UtilityMethods.SUCCESS_KEY: True,
                }
            else:
                raise BusinessPost.DoesNotExist()
        except BusinessPost.DoesNotExist:
            data = {
                 UtilityMethods.ERROR_KEY: 'Wrong ID'
            }
        except DataValidationError as e:
            data = {
                UtilityMethods.ERROR_KEY: e.args[1]
            }
        return Response(data=response_data, status=status)

##
class BusinessCategoryList(APIView):
     def post(self, request):
        status, response_data = UtilityMethods.get_default_response()
        categorylist = BusinessCategory.objects.all()
        serializer = BusinessPostCategorySerializer(categorylist, many=True)
        return Response(data=serializer.data, status=status)


