from django.db import models

# Create your models here.

# Modelo Cliente
class Cliente(models.Model):

    # Definición de atributos
    id_cliente = models.AutoField(primary_key=True)
    identificacion = models.CharField(max_length=15)
    apellido = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    direccion = models.TextField()
    fecha_nacimiento = models.DateField()
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.apellido} {self.nombre}"


# Modelo Vehiculo
class Vehiculo(models.Model):

    # Definición de atributos
    id_vehiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=10)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30)

    # Relación con cliente
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.placa} - {self.marca}"



class Estacionamiento(models.Model):

    # Definición de atributos
    id_estacionamiento = models.AutoField(primary_key=True)
    numero_espacio = models.IntegerField()
    fecha_ingreso = models.DateTimeField()
    fecha_salida = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20)

    # Relación con vehículo
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Espacio {self.numero_espacio}"


# Modelo Facturacion
class Facturacion(models.Model):

    # Definición de atributos
    id_factura = models.AutoField(primary_key=True)
    fecha_factura = models.DateField()
    total = models.DecimalField(max_digits=8, decimal_places=2)
    metodo_pago = models.CharField(max_length=30)

    # Relación con estacionamiento
    estacionamiento = models.ForeignKey(
        Estacionamiento,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Factura #{self.id_factura}"