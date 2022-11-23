from django.db import models
from student.models import Student
from course.models import Course


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='result_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='result_course')
    score = models.FloatField()

    class Meta:
        ordering = ['id']
