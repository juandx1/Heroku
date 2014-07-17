from django import forms
from django.forms import ModelForm
from App.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email' , 'password')
        widgets = {
            'first_name' : forms.TextInput(attrs={'class':'nombre-izquierda','required':'required', 'placeholder':'Nombre'}),
            'last_name': forms.TextInput(attrs={'class':'nombre-derecha','required':'required', 'placeholder':'Apellido'}),
            'email': forms.EmailInput(attrs={'required':'required', 'placeholder':'Email'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('fecha_nacimiento', 'genero', 'telefono', 'iglesia')
        widgets ={
            'fecha_nacimiento' : forms.TextInput(attrs={'id':'fecha','class':'fecha','required':'required','placeholder':'Fecha de Nacimiento'}),
            'genero':forms.Select(attrs={'required':'required','placeholder':'Genero'}),
            'telefono':forms.NumberInput(attrs={'placeholder':'Telefono'}),
            'iglesia':forms.Select(attrs={'placeholder':'Iglesia'})
        }



class ImagenForm(forms.ModelForm):
     class Meta:
        model = Foto
        fields = ('imagen',)
        widgets = {
            'imagen':forms.FileInput(attrs={'required': 'required','style':'position:absolute;','class':'file-input','accept':'image/*'})
        }


class AlbumForm(forms.ModelForm):
     class Meta:
        model = Album
        fields = ('nombre','descripcion')




class PostForm(forms.ModelForm):
     user = forms.IntegerField(widget=forms.HiddenInput())

     class Meta:
        model = Post
        fields = ('contenido',)
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'estado','placeholder':'¿Escribe algo?', 'rows': 0 }),
        }


class ComentarioForm(forms.ModelForm):
     id = forms.IntegerField(widget=forms.HiddenInput())
     class Meta:
        model = Comentario
        fields = ('contenido',)
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'texto-comentario-usuarios','placeholder':'Escribir comentario','rows': 0 }),
        }

class ImageUploadForm(forms.Form):
    foto_perfil = forms.ImageField()
    foto_cover = forms.ImageField()

