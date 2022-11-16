from result.models import Result
from rest_framework import serializers


class ResultSerializer(serializers.ModelSerializer):

    class Meta:

        model = Result
        fields = ['id', 'student', 'course', 'score']

    def validate(self, data):
        student = data.get('student')
        course = data.get('course')
        assigned_teacher_id = course.course_teacher.user.id
        request = self.context['request']
        is_enrolled = student.enrolled_course.filter(id=course.id).exists()
        is_present = Result.objects.filter(course=course, student=student).exists()
        if request.method == 'POST' and is_present:
            raise serializers.ValidationError("Result Already Present, Update if required")
        if is_enrolled and int(assigned_teacher_id) == int(request.user.id):
            return data
        raise serializers.ValidationError("Wrong Input of Result Parameters")
