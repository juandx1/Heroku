from django.contrib import admin
from Contabilidad.models import *
# Register your models here.

class GrupoInline(admin.TabularInline):
    model=Grupo
    extra=1


class CuentaAdmin(admin.ModelAdmin):
    list_display = ('pk','iglesia', 'tipo',)
    inlines = [GrupoInline]

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'cuenta',)

class ConceptoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'numero', 'nombre', 'grupo')

class RegistroAdmin(admin.ModelAdmin):
    list_display = ('pk', 'numero','fecha','comentario','deposito','retiro')




admin.site.register(Cuenta,CuentaAdmin)
admin.site.register(Grupo,GrupoAdmin)
admin.site.register(Concepto,ConceptoAdmin)
admin.site.register(Registro,RegistroAdmin)
