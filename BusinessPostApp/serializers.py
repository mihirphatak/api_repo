from rest_framework.serializers import ModelSerializer

from BusinessPostApp.models import BusinessPost, BusinessCategory, BusinessPoints


class BusinessPostSerializer(ModelSerializer):
    class Meta:
        model = BusinessPost
        fields = '__all__'


class BusinessPostCategorySerializer(ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = '__all__'


class BusinessPostPointSerializer(ModelSerializer):
    class Meta:
        model = BusinessPoints
        fields = '__all__'
