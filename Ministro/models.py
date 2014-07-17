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


class grupo(models.Model):
    nombre = models.CharField(max_length=100)
    cuenta=models.ForeignKey(Cuenta)

# Create your models here.

class Usuario_Ministro(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=140,blank=True, null=True)
    telefono = models.IntegerField(blank=True,null=True, max_length=15)
    direccion = models.CharField(max_length=200,blank=True, null=True)
    barrio = models.CharField(max_length=100,blank=True, null=True)
    profesion = models.CharField(max_length=200, blank=True, null=True)
    cedula = models.CharField(max_length=150, blank=True, null=True)
    ocupacion = models.CharField(max_length=200, blank=True, null=True)
    bautizado = models.BooleanField(default=False)
    ciudad = models.CharField(max_length=200, blank=True, null=True)
    pais = models.CharField(max_length=200, blank=True, null=True)

