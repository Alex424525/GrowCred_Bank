from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20, unique=True)
    birthdate = models.DateField()
    address = models.CharField(max_length=255)


    def __str__(self):
        return self.username
