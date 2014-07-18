from django.contrib import admin
from Ministro.models import *
# Register your models here.

class Usuario_Ministro_Admin(admin.ModelAdmin):
    list_display = ('nombre','apellido','email','telefono','direccion','barrio','profesion','cedula','ocupacion','bautizado','ciudad','pais',)

class Campo_Personalizado_Admin(admin.ModelAdmin):
    list_display = ('nombre', 'iglesia',)

class Contenido_Campo_Admin(admin.ModelAdmin):
    list_display = ('contenido','campo','usuario',)

class Rango_Admin(admin.ModelAdmin):
    list_display = ('nombre','descripcion','iglesia','usuario')


admin.site.register(Usuario_Ministro,Usuario_Ministro_Admin)
admin.site.register(Campo_Personalizado,Campo_Personalizado_Admin)
admin.site.register(Contenido_Campo_Personalizado,Contenido_Campo_Admin)
admin.site.register(Rango,Rango_Admin)