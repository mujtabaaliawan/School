from .models import Staff
from rest_framework import serializers
from user_profile.serializers import UserSerializer


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Staff
        fields = ['id', 'user', 'role']

    def create(self, validated_data):
        user = UserSerializer.create(self, validated_data=validated_data)
        staff, created = Staff.objects.update_or_create(user=user)
        return staff

    def to_representation(self, instance):
        representation = dict()
        representation['Staff ID'] = instance.id
        representation['Staff Name'] = instance.user.first_name
        representation['Staff Email'] = instance.user.email
        return representation
