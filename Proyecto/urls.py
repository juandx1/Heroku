from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from App.views import *
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Proyecto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #Modulo Administrador
    url(r'^admin/', include(admin.site.urls)),

    #Modulo Inicio
    url(r'^register/$', register, name='register'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^home/$', home, name='home'),
    url(r'^confirmacion/$', confirmacion , name='confirmacion'),

    #Modulo Perfil
    url(r'^perfil/$', perfil, name='perfil'),
    url(r'^$', home, name='home'),
    url(r'^delete/post/(\d+)$', eliminar_post, name='eliminar_post'),
    url(r'^crear/post/$', nuevo_post, name='nuevo_post'),
    url(r'^crear/comentario/$', nuevo_comentario, name='nuevo_comentario'),
    url(r'^ajax/post/', ajax_post, name='ajax_post'),

    #Modulo Fotos
    url(r'^foto/(\d+)$', editar_Foto, name='foto'),
    url(r'^delete/foto/(\d+)$', eliminar_Foto, name='eliminar_foto'),
    url(r'^perfil/foto/(\d+)$', perfil_foto, name='establecer_foto_perfil'),
    url(r'^cover/foto/(\d+)$', cover_foto, name='establecer_foto_cover'),
    url(r'^delete/album/(\d+)$', eliminar_album, name='eliminar_album'),
    url(r'^album/(\d+)$', editar_album, name='album'),
    url(r'^albumes/(\d+)$', albumes, name='albumes'),
    url(r'^ver/albumes/(\d+)$', ver_albumes, name='ver_albumes'),
    url(r'^ver/album/(\d+)/(\d+)$', ver_album, name='ver_album'),
    url(r'^ver/foto/(\d+)$', ver_foto, name='ver_foto'),
    url(r'^fotos/$', fotos, name='fotos'),
    url(r'^subir/foto/$', subir_foto_album, name='subir_foto_album'),
    url(r'^crear/album/$', crear_album, name='crear_album'),

    #Modulo Amigos
    url(r'^amigos/$', amigos, name='amigos'),
    url(r'^ver/amigos/(\d+)$', ver_amigos, name='ver_amigos'),
    url(r'^solicitud/amistad$', solicitud_pendiente, name='solicitud_amistad'),
    url(r'^invitacion/amistad$', invitacion_pendiente, name='invitacion_pendiente'),
    url(r'^delete/amigo/(\d+)$', eliminar_amigo, name='eliminar_amigo'),
    url(r'^ver/usuario/(\d+)$', ver_usuario, name='ver_usuario'),
    url(r'^add/amigo/(\d+)$', agregar_amigo, name='agregar_amigo'),
    url(r'^aceptar/amigo/(\d+)$', aceptar_amigo, name='aceptar_amigo'),
    url(r'^delete/comentario/(\d+)$', eliminar_comentario, name='eliminar_comentario'),
    url(r'^delete/contacto/(\d+)$', eliminar_contacto, name='eliminar_contacto'),
    url(r'^ajax/amigos/', ajax_amigos, name='ajax_amigos'),
    url(r'^ajax/ver/amigos/', ajax_ver_amigos, name='ajax_amigos'),

    #Modulo mensajes
    url(r'^mensajes/$', mensajes, name='mensajes'),
    url(r'^enviados/$', enviados, name='enviados'),
    url(r'^mensaje/(\d+)$', mensaje, name='mensaje'),
    url(r'^delete/mensaje/(\d+)$', eliminar_mensaje, name='eliminar_mensaje'),
    url(r'^nuevo/mensaje/$', nuevo_mensaje , name='nuevo_mensaje'),
    url(r'^enviar/mensaje/$', enviar_mensaje , name='enviar_mensaje'),
    url(r'^ajax/destinatarios/', ajax_destinatarios, name='ajax_destinatarios'),
    url(r'^ajax/destinatario/(\d+)$', ajax_destinatario, name='ajax_destinatario'),

    #Modulo Eventos
     url(r'^eventos/$', eventos, name='eventos'),
     url(r'^eventos/asistidos$', eventos_asistidos, name='eventos_asistidos'),
     url(r'^eventos/pendientes$', eventos_pendientes, name='eventos_pendientes'),
     url(r'^editar/evento/(\d+)$', editar_evento , name='editar_evento'),
     url(r'^crear/evento/$', crear_evento , name='crear_evento'),


)+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

