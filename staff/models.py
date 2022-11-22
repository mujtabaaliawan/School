from user_profile.models import User
from django.db import models


class Staff(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, default='staff')
    mobile_number = models.CharField(max_length=20, default='0')

    class Meta:
        ordering = ['id']

