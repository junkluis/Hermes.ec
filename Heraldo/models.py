from pyexpat import model
from django.contrib.auth.models import User
from django.db import models
import datetime


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
    capacity = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    measurement = models.CharField(
        max_length=2,
        choices=ROL_CHOICES_UNIT,
        default='Kg',
    )
    color = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    lat = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    log = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    is_active = models.BooleanField(default=True)

class Order(models.Model):
    ORDER_STATUS = [
        ('PD', 'Pendiente'),
        ('EP', 'En Proceso'),
        ('FN', 'Finalizado'),
        ('CN', 'Cancelado'),
    ]
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conductor')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client')
    truck = models.ForeignKey('Truck', on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=255)
    origin =  models.CharField(max_length=255)
    origin_coord_lat =  models.CharField(max_length=255)
    origin_coord_long =  models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    destination_coord_lat = models.CharField(max_length=255)
    destination_coord_long = models.CharField(max_length=255)
    location_coord_lat = models.CharField(max_length=255, blank=True, null=True)
    location_coord_long = models.CharField(max_length=255, blank=True, null=True)
    location_update = models.DateTimeField(auto_now=True)
    peso = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    tarifa = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    precio = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    distancia = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    status = models.CharField(
        max_length=2,
        choices=ORDER_STATUS,
        default='PD',
    )
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=250)
    latitud = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    longitud = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)

class Tarifas(models.Model):
    toneladas_seis = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    toneladas = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    toneladas_diez = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    kilogramos = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)
    libras = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=8)

