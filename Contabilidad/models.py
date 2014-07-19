from django.db import models
from App.models import *

# Create your models here.
class Cuenta(models.Model):
    TIPO = (
        ('A', 'Activo'),
        ('P', 'Pasivo'),
        ('C', 'Capital'),
    )
    tipo=models.CharField(max_length=1, choices=TIPO)
    iglesia=models.ForeignKey(Iglesia)

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    cuenta=models.ForeignKey(Cuenta)

class Concepto(models.Model):
    numero = models.IntegerField()
    nombre = models.CharField(max_length=100)
    grupo = models.ForeignKey(Grupo)

class Registro(models.Model):
    numero=models.IntegerField()
    fecha=models.DateField()
    comentario=models.CharField(max_length=140)
    deposito=models.IntegerField()
    retiro=models.IntegerField()

# Create your models here.
