from course.models import Course
from user_profile.models import User
from django.db import models


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    choice = (
        ("student", "STUDENT"),
        )
    role = models.CharField(max_length=10, choices=choice, default="STUDENT")
    enrolled_course = models.ManyToManyField(Course)

    def __str__(self):
        return f'{self.id}' + ' ' + f'{self.user.email}'







