from django.contrib import admin
from .models import Rol, Driver, DriverStatus

# Register your models here.
admin.site.register(Rol)
admin.site.register(Driver)
admin.site.register(DriverStatus)