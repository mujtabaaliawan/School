from course.models import Course
from user_profile.models import User
from django.db import models


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, default='student')
    mobile_number = models.CharField(max_length=20, default='0')
    enrolled_course = models.ManyToManyField(Course, blank=True)

    class Meta:
        ordering = ['id']









