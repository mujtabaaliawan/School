from userprofile.models import User
from django.db import models


class Teacher(models.Model):

    base_profile = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.id}' + ' ' + f'{self.base_profile.email}'
