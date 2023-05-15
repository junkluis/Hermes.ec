from django.contrib.auth.models import User
from django.db import models


class Rol(models.Model):
    ROL_CHOICES = [
        ('AD', 'Admin'),
        ('DR', 'Drive'),
        ('CL', 'Client'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_rol = models.CharField(
        max_length=2,
        choices=ROL_CHOICES,
        default='CL',
    )

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    identification = models.CharField(max_length=30)
    license_number = models.CharField(max_length=100)
    status = models.ForeignKey('DriverStatus', on_delete=models.CASCADE)

class DriverStatus(models.Model):
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=300)

