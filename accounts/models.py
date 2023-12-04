from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=2, choices={
        ('M', 'Male'),
        ('F', 'Female')
    }, null=True, blank=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)


