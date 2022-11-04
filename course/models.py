from django.db import models
from teacher.models import Teacher


class Course(models.Model):

    course_title = models.CharField(max_length=255)
    teacher_profile = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='course_teacher')

    def __str__(self):
        return f'{self.course_title}'
