from django.db import models
from teacher.models import Teacher


class Course(models.Model):

    course_title = models.CharField(max_length=255)
    course_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subject_teacher')
