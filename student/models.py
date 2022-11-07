from course.models import Course
from user_profile.models import User
from django.db import models


class Student(models.Model):

    base_profile = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)
    enrolled_course = models.ManyToManyField(Course)

    def __str__(self):
        return f'{self.id}' + ' ' + f'{self.base_profile.email}'







