from user_profile.models import User
from django.db import models


class Admin(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=20, default='0')

    def __str__(self):
        return f'{self.id}' + ' ' + f'{self.user.email}'