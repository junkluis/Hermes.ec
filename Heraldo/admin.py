from django.contrib import admin
from .models import *

@admin.register(Rol)
class Rol(admin.ModelAdmin):
    list_display = ('id','user_rol', 'user')

@admin.register(Driver)
class Driver(admin.ModelAdmin):
    list_display = ('id', 'user')

@admin.register(DriverStatus)
class DriverStatus(admin.ModelAdmin):
    list_display = ('id', 'status', 'description')

@admin.register(Truck)
class Truck(admin.ModelAdmin):
    list_display = ('id', 'user', 'license', 'status', 'is_active')

@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ('id', 'driver', 'client', 'content', 'status', 'peso', 'tarifa', 'precio', 'distancia', 'is_active')

@admin.register(Ubicacion)
class Ubicacion(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'latitud', 'longitud')

@admin.register(Tarifas)
class Tarifas(admin.ModelAdmin):
    list_display = ('id', 'toneladas_seis', 'toneladas', 'toneladas_diez', 'kilogramos', 'libras')

@admin.register(Console)
class Console(admin.ModelAdmin):
    list_display = ('id', 'name', 'archivo')

@admin.register(ConsolePicture)
class ConsolePicture(admin.ModelAdmin):
    list_display = ('id', 'filename', 'mimetype')

@admin.register(OrdersFile)
class OrdersFile(admin.ModelAdmin):
    list_display = ('id', 'orden', 'archivo', 'nombre')

@admin.register(changePasswordToken)
class changePasswordToken(admin.ModelAdmin):
    list_display = ('id', 'user', 'creation_date')

@admin.register(Formulario)
class Formulario(admin.ModelAdmin):
    list_display = ('id', 'orden', 'fecha', 'observacion', 'foto', 'entregado_a', 'tipo')

    

