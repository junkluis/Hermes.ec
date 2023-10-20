from pyexpat import model
from django.contrib.auth.models import User
from django.db import models
import datetime
from db_file_storage.model_utils import delete_file, delete_file_if_needed


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
        ('Tn', 'Toneladas'),
    ]
    duenio = models.CharField(max_length=100, default='TRANSPFLOR S.A')
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
    color_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, default='Disponible')
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

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
    peso = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=6)
    tarifa = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=6)
    precio = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=6)
    distancia = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=6)
    status = models.CharField(
        max_length=2,
        choices=ORDER_STATUS,
        default='PD',
    )
    unidad = models.CharField(max_length=10, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    order_file = models.ForeignKey('Console', on_delete=models.CASCADE, blank=True, null=True)
    tiempo_partida=models.DateTimeField(blank=True, default=datetime.datetime.now)
    
class OrdersFile(models.Model):
    orden = models.ForeignKey('Order', on_delete=models.CASCADE)
    archivo = models.ForeignKey('Console', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=250)


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


class ConsolePicture(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)

class Console(models.Model):
    name = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='Heraldo.ConsolePicture/bytes/filename/mimetype', blank=True, null=True)

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'picture')
        super(Console, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Console, self).delete(*args, **kwargs)
        delete_file(self, 'picture')
    
class changePasswordToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    cp_token = models.CharField(max_length=255)


class Formulario(models.Model):
    TYPE_CHOICES = [
        ('Imprevisto', 'Reporte de Imprevisto'),
        ('Confirmacion', 'Confirmacion de entrega'),
    ]
    orden = models.ForeignKey('Order', on_delete=models.CASCADE)
    fecha = models.DateTimeField(blank=True, null=True)
    observacion = models.CharField(max_length=225)
    foto = models.ForeignKey('Console', on_delete=models.CASCADE, blank=True, null=True)
    entregado_a = models.CharField(max_length=225, blank=True, null=True)
    tipo =  models.CharField(
        max_length=12,
        choices=TYPE_CHOICES,
        default='Confirmacion',
    )

    