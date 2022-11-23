from result.models import Result
from rest_framework import serializers
from student.serializers import StudentSerializer
from course.serializers import CourseSerializer
from student.models import Student
from course.models import Course


class ResultSerializer(serializers.ModelSerializer):

    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source='student', write_only=True)

    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True)

    class Meta:

        model = Result
        fields = '__all__'

    def validate(self, data):
        student = data.get('student')
        course = data.get('course')
        assigned_teacher_id = course.course_teacher.user.id
        request = self.context['request']
        is_enrolled = student.enrolled_course.filter(id=course.id).exists()
        is_present = Result.objects.filter(course=course, student=student).exists()
        if request.method == 'POST' and is_present:
            raise serializers.ValidationError("Result Already Present, Update if required")
        if is_enrolled and assigned_teacher_id == request.user.id or request.user.is_superuser:
            return data
        raise serializers.ValidationError("Wrong Input of Result Parameters")
