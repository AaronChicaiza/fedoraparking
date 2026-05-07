from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal

# Modelo Cliente
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    identificacion = models.CharField(max_length=15, unique=True)
    apellido = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    direccion = models.TextField()
    fecha_nacimiento = models.DateField()
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.apellido} {self.nombre}"
    
# Modelo Vehiculo
class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30)

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.placa} - {self.marca}"

# Modelo Espacio
class Espacio(models.Model):
    ESTADOS = [
        ('libre', 'Libre'),
        ('ocupado', 'Ocupado'),
    ]

    id_espacio = models.AutoField(primary_key=True)
    numero = models.IntegerField(unique=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='libre')

    def __str__(self):
        return f"Espacio {self.numero} - {self.estado}"

# Modelo Tarifa
class Tarifa(models.Model):
    id_tarifa = models.AutoField(primary_key=True)
    precio_por_hora = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Tarifa: ${self.precio_por_hora}/hora"

# Modelo Estacionamiento
class Estacionamiento(models.Model):
    id_estacionamiento = models.AutoField(primary_key=True)
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    fecha_salida = models.DateTimeField(null=True, blank=True)

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)

    #CAMBIO IMPORTANTE AQUÍ
    espacio = models.ForeignKey(
        Espacio,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    tarifa = models.ForeignKey(Tarifa, on_delete=models.CASCADE)

    def clean(self):
        if self.fecha_salida and self.fecha_salida <= self.fecha_ingreso:
            raise ValidationError("La fecha de salida debe ser posterior a la fecha de ingreso.")

        if self.espacio and self.espacio.estado == 'ocupado':
            raise ValidationError("El espacio seleccionado está ocupado.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def tiempo_estacionado(self):
        if self.fecha_salida:
            return self.fecha_salida - self.fecha_ingreso
        return timezone.now() - self.fecha_ingreso

    def calcular_costo(self):
        if self.fecha_salida:
            horas = self.tiempo_estacionado().total_seconds() / 3600
            return Decimal(horas) * self.tarifa.precio_por_hora
        return Decimal(0)

    def __str__(self):
        return f"Ticket {self.id_estacionamiento}"

# Modelo Facturacion
class Facturacion(models.Model):
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ]

    id_factura = models.AutoField(primary_key=True)
    fecha_factura = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    metodo_pago = models.CharField(max_length=30, choices=METODOS_PAGO)

    estacionamiento = models.OneToOneField(Estacionamiento, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.total = self.estacionamiento.calcular_costo()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura #{self.id_factura} - ${self.total}"