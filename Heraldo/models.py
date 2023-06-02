from django.contrib.auth.models import User
from django.db import models


class Rol(models.Model):
    ROL_CHOICES = [
        ('AD', 'Admin'),
        ('DR', 'Drive'),
        ('CL', 'Client'),
        ('NN', 'None'),
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

class Truck(models.Model):
    ROL_CHOICES_UNIT = [
        ('Kg', 'Kilogram'),
        ('Lb', 'Pound'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    license = models.CharField(max_length=100)
    capacity = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    measurement = models.CharField(
        max_length=2,
        choices=ROL_CHOICES_UNIT,
        default='Kg',
    )
    color = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


