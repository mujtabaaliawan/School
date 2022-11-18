from .models import Course
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'course_title', 'course_teacher']

    def to_representation(self, instance):
        representation = dict()
        representation["Course ID"] = instance.id
        representation["Course Title"] = instance.course_title
        representation["Teacher ID"] = instance.course_teacher.id
        representation["Teacher Name"] = instance.course_teacher.user.first_name
        representation["Teacher Email"] = instance.course_teacher.user.email
        return representation


