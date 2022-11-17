from .models import Admin
from rest_framework import serializers
from user_profile.serializers import UserSerializer


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Admin
        fields = ['id', 'user', 'role', 'mobile_number']

    def create(self, validated_data):
        user = UserSerializer.create(self, validated_data=validated_data)
        staff, created = Admin.objects.update_or_create(user=user)
        return staff

    def to_representation(self, instance):
        representation = dict()
        representation['Staff ID'] = instance.id
        representation['Staff User ID'] = instance.user.id
        representation['Staff Name'] = instance.user.first_name
        representation['Staff Email'] = instance.user.email
        representation['Staff Mobile Number'] = instance.user.email

        return representation
