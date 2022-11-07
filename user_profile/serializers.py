from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        password = validated_data.get('password')
        base_user = User.objects.create_user(email=email, first_name=first_name, password=password)
        return base_user
