from result.models import Result
from rest_framework import serializers


class ResultSerializer(serializers.ModelSerializer):

    class Meta:

        model = Result
        fields = ['student', 'course', 'score']

    def validate(self, data):

        student = data.get('student')
        course_id = data.get('course').id
        is_enrolled = student.enrolled_course.filter(id=course_id).exists()
        if is_enrolled:
            return data
        raise serializers.ValidationError("Course Not Enrolled")
