from .models import Student
from rest_framework import serializers
from user_profile.serializers import UserSerializer
from course.models import Course
from result.models import Result


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:

        model = Student
        fields = ['id', 'user', 'role', 'mobile_number', 'enrolled_course']
        extra_kwargs = {
            'enrolled_course': {'read_only': True}
        }

    def create(self, validated_data):
        user = UserSerializer.create(self, validated_data=validated_data)
        student, created = Student.objects.update_or_create(user=user)
        return student

    def to_representation(self, instance):
        representation = dict()
        representation["ID"] = instance.id
        representation["Name"] = instance.user.first_name
        representation["Email"] = instance.user.email
        representation["Mobile Number"] = instance.mobile_number
        representation["User ID"] = instance.user.id
        course_count = 0
        course_detail = dict()
        for subject in instance.enrolled_course.all():
            enrolled_courses = dict()
            course_count = course_count + 1
            enrolled_courses["Course ID"] = subject.id
            enrolled_courses["Course Title"] = subject.course_title
            enrolled_courses["Course Teacher ID"] = subject.course_teacher.id
            enrolled_courses["Course Teacher Name"] = subject.course_teacher.user.first_name
            enrolled_courses["Course Teacher Email"] = subject.course_teacher.user.email
            course_result = Result.objects.filter(student=instance).filter(course=subject)
            if course_result.exists():
                enrolled_courses["Course Marks"] = course_result[0].score
            else:
                enrolled_courses["Course Marks"] = 'Result not entered'
            course_detail[course_count] = enrolled_courses
        representation['Enrolled Courses'] = course_detail
        return representation


class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Student
        fields = ['id', 'enrolled_course']

    def update(self, instance, validated_data):
        course = validated_data.get('enrolled_course')
        instance.enrolled_course.add(course[0])
        return instance


class EnrollmentAdminSerializer(serializers.ModelSerializer):

    class Meta:

        model = Student
        fields = ['id', 'enrolled_course']
