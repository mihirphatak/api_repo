from rest_framework.serializers import ModelSerializer

from UserApp.models import User


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        u_fields = User.FieldNames
        fields = (u_fields.first_name, u_fields.last_name, u_fields.contact_number, u_fields.email)
