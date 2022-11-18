from .models import Teacher
from rest_framework import serializers
from user_profile.serializers import UserSerializer
from course.models import Course
from student.models import Student
from result.models import Result


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:

        model = Teacher
        fields = ['id', 'user', 'role', 'mobile_number']

    def create(self, validated_data):
        user = UserSerializer.create(self, validated_data=validated_data)
        role = validated_data.get('role')
        mobile_number = validated_data.get('mobile_number')
        teacher, created = Teacher.objects.update_or_create(user=user, role=role, mobile_number=mobile_number)
        return teacher

    def to_representation(self, instance):
        representation = dict()
        courses = Course.objects.filter(course_teacher=instance.id)
        representation['Teacher ID'] = instance.id
        representation['Teacher Name'] = instance.user.first_name
        representation['Teacher Email'] = instance.user.email
        representation['Teacher Mobile Number'] = instance.mobile_number
        representation['Teacher User ID'] = instance.user.id
        taught_courses = dict()
        course_count = 1
        for subject in courses:
            course_detail = dict()
            course_detail['Course ID'] = subject.id
            course_detail['Course Title'] = subject.course_title
            students_data = Student.objects.all().filter(enrolled_course=subject)
            students_count = 1
            course_students = dict()
            for stud in students_data:
                students = dict()
                students['Student ID'] = stud.id
                students['Student Name'] = stud.user.first_name
                students['Student Email'] = stud.user.email
                course_result = Result.objects.filter(student=stud).filter(course=subject)
                if course_result.exists():
                    students["Result ID"] = course_result[0].id
                    students["Marks"] = course_result[0].score
                else:
                    students["Marks"] = 'Result not entered'
                course_students[students_count] = students
                students_count = students_count + 1
            course_detail['Students'] = course_students
            taught_courses[course_count] = course_detail
            course_count = course_count + 1
        representation['Subjects'] = taught_courses
        return representation


class TeacherBasicSerializer(serializers.ModelSerializer):

    class Meta:

        model = Teacher
        fields = ['id', 'user', 'role', 'mobile_number']

    def to_representation(self, instance):
        representation = dict()
        courses = Course.objects.filter(course_teacher=instance.id)
        representation['Teacher ID'] = instance.id
        representation['Teacher Name'] = instance.user.first_name
        representation['Teacher Email'] = instance.user.email
        taught_courses = dict()
        course_count = 1
        for subject in courses:
            course_detail = dict()
            course_detail['Course ID'] = subject.id
            course_detail['Course Title'] = subject.course_title
            taught_courses[course_count] = course_detail
            course_count = course_count + 1
        representation['Teacher Subjects'] = taught_courses
        return representation


