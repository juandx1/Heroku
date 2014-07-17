from django.contrib import admin
from App.models import *
# Register your models here.

class ContactoInline(admin.TabularInline):
    model=Contacto
    extra=1
    fk_name = 'fuente'

class ComentarioInline(admin.TabularInline):
    model=Comentario
    extra=1

class InvitacionInline(admin.TabularInline):
    model=Invitacion
    extra=1

class MensajeInline(admin.TabularInline):
    model=Mensaje
    extra=1
    fk_name = 'de'

class AlbumInline(admin.TabularInline):
    model=Album
    extra=1

class FotoInline(admin.TabularInline):
    model=Foto
    extra=1

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'fecha_nacimiento', 'genero', 'pais', 'telefono','iglesia',)
    inlines = [ContactoInline, MensajeInline, AlbumInline]

class IglesiaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'direccion', 'nombre', 'telefono', 'url',)

class ContactoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fuente', 'destino',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'destino','fuente')
    inlines = [ComentarioInline]

class EventoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'usuario','fecha_inicio','fecha_fin',)
    inlines = [InvitacionInline]

class MensajeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'de', 'para','fecha_envio')

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('pk','usuario')
    inlines = [FotoInline]

class InvitacionAdmin(admin.ModelAdmin):
    list_display = ('pk','usuario')



admin.site.register(Usuario,UsuarioAdmin)
admin.site.register(Iglesia,IglesiaAdmin)
admin.site.register(Contacto,ContactoAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Evento,EventoAdmin)
admin.site.register(Mensaje,MensajeAdmin)
admin.site.register(Album,AlbumAdmin)
admin.site.register(Invitacion,InvitacionAdmin)

