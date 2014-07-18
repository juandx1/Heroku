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
    desposito=models.IntegerField()
    retiro=models.IntegerField()




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


class Campo_Personalizado(models.Model):
    nombre = models.CharField(max_length=100)
    iglesia = models.ForeignKey(Iglesia)

class Contenido_Campo_Personalizado(models.Model):
    contenido = models.CharField(max_length=200)
    campo = models.ForeignKey(Campo_Personalizado)
    usuario = models.ForeignKey(Usuario_Ministro)

class Rango(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    iglesia = models.ForeignKey(Iglesia)
    usuario = models.ForeignKey(Usuario_Ministro)