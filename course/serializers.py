from .models import Course
from rest_framework import serializers
from teacher.serializers import TeacherSerializer


class CourseListSerializer(serializers.ModelSerializer):

    course_teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
