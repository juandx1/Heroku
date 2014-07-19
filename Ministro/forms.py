from django import forms
from django.forms import ModelForm
from Ministro.models import *

class Usuario_Ministro_Form(forms.ModelForm):
    class Meta:
        model = Usuario_Ministro
        fields = ('nombre', 'apellido', 'email', 'telefono', 'direccion', 'barrio', 'profesion', 'cedula', 'ocupacion', 'bautizado', 'ciudad', 'pais',)

class Campo_Form(forms.ModelForm):
    iglesia = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = Campo_Personalizado
        fields = ('nombre', )

class Contenido_Campo_Form(forms.ModelForm):
    usuario = forms.IntegerField(widget=forms.HiddenInput)
    campo = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = Contenido_Campo_Personalizado
        fields = ('contenido',)

class Rango(forms.ModelForm):
    iglesia = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = Rango
        fields = {'nombre','descripcion',}

