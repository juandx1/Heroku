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
