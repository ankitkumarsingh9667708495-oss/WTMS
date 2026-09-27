from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('driver', 'Driver')
    ]

    role =  models.CharField(max_length=20, choices=ROLES, default='staff')

    def __str__(self):
        return self.username