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
            response_data = {
                UtilityMethods.SUCCESS_KEY: True,
                UtilityMethods.MESSAGE_KEY: serializer.data
            }
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
        return Response(data=response_data, status=status)