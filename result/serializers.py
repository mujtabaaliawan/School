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
        user_id = self.context['request'].user.id
        is_enrolled = student.enrolled_course.filter(id=course.id).exists()
        print(is_enrolled)
        if is_enrolled and int(assigned_teacher_id) == int(user_id):
            return data
        raise serializers.ValidationError("Wrong Input of Result Parameters")
