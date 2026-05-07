from django.contrib import admin
#Importando el MOdelo Cliente
from.models import Cliente
from.models import Vehiculo
from.models import Estacionamiento
from.models import Facturacion

# Register your models here.
#Haciendo Crud Automactico de Cliente
admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Estacionamiento)
admin.site.register(Facturacion)

