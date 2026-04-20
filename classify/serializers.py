from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class GetUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'gender', 'age', 'age_group', 'country_id']