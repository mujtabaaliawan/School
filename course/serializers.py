from .models import Course
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'course_title', 'course_teacher']

    def to_representation(self, instance):
        representation = dict()
        representation["course_id"] = instance.id
        representation["course_title"] = instance.course_title
        representation["teacher_id"] = instance.course_teacher.id
        representation["teacher_name"] = instance.course_teacher.user.first_name
        representation["teacher_email"] = instance.course_teacher.user.email
        return representation


