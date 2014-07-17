
from App.forms import ComentarioForm
from App.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_imagen_cover(user):
    try:
        al=Album.objects.get(usuario=user,tipo='C')
        cover=Foto.objects.get(album=al,tipo='C')
    except:
        cover=1

    return cover

def get_imagen_perfil(user):

    try:

        al=Album.objects.get(usuario=user,tipo='P')

        perfil=Foto.objects.get(album=al,tipo='P')
    except:
         perfil=1

    return perfil

def get_lista_posts(user):

    listaPosts = []
    posts=Post.objects.filter(destino=user).order_by('-fecha_publicacion')
    paginator = Paginator(posts, 10) # muestra 10 post por pagina
    posts=paginator.page(1)

    for i in posts:
        comentarios=[]
        formComentario=ComentarioForm(initial={'id':i.pk,'usuario':user})

        try:
            al2=Album.objects.get(usuario=i.fuente,tipo='P')
            foto_perfil=Foto.objects.get(album=al2,tipo='P')
        except:
            foto_perfil=1

        for j in Comentario.objects.filter(post=i):
            try:
                al3=Album.objects.get(usuario=j.usuario,tipo='P')
                foto=Foto.objects.get(album=al3,tipo='P')
            except:
                foto=1
            a={
                'comentario':j,
                'foto':foto,
            }
            comentarios.append(a)
        d={
            'post':i,
            'comentarios':comentarios,
            'form': formComentario,
            'foto':foto_perfil,
        }
        listaPosts.append(d)

    return listaPosts

def get_lista_posts_ajax(user,page):

    listaPosts = []
    posts=Post.objects.filter(destino=user).order_by('-fecha_publicacion')
    paginator = Paginator(posts, 10) # muestra 10 post por pagina
    posts=paginator.page(page)

    for i in posts:
        comentarios=[]
        formComentario=ComentarioForm(initial={'id':i.pk})
        try:
            al2=Album.objects.get(usuario=i.fuente,tipo='P')
            foto_perfil=Foto.objects.get(album=al2,tipo='P')
        except:
            foto_perfil=1

        for j in Comentario.objects.filter(post=i):
            try:
                al3=Album.objects.get(usuario=j.usuario,tipo='P')
                foto=Foto.objects.get(album=al3,tipo='P')
            except:
                foto=1
            a={
                'comentario':j,
                'foto':foto,
            }
            comentarios.append(a)
        d={
            'post':i,
            'comentarios':comentarios,
            'form': formComentario,
            'foto':foto_perfil,
        }
        listaPosts.append(d)

    return listaPosts

def get_lista_albumes(user):
    albumes=Album.objects.filter(usuario=user.usuario)
    listaAlbumes = []
    for i in albumes:
        fotos=[]
        for j in Foto.objects.filter(album=i):
            a={
                'foto':j,
            }
            fotos.append(a)
        d={
            'album':i,
            'fotos':fotos,
        }
        listaAlbumes.append(d)

    return listaAlbumes

def get_lista_amigos(user):
    contactos=Contacto.objects.filter(fuente=user).exclude(fecha_aceptacion=None)
    amigos=[]
    for i in contactos:
        amigo=i.destino
        al=Album.objects.get(usuario=amigo,tipo='P')
        try:
            foto=Foto.objects.get(album=al,tipo='P')
        except:
            foto=1
        a={
            'contacto':i,
            'foto':foto
        }
        amigos.append(a)


    return amigos

def get_lista_aceptacion_pendiente(request):
    contactos=Contacto.objects.filter(destino=request.user,fecha_aceptacion=None,original=True)
    amigos=[]

    for i in contactos:
        amigo=i.fuente
        al=Album.objects.get(usuario=amigo,tipo='P')
        try:
            foto=Foto.objects.get(album=al,tipo='P')
        except:
            foto=1
        a={
            'contacto':i,
            'foto':foto
        }
        amigos.append(a)


    return amigos

def get_lista_invitacion_pendiente(request):
    contactos=Contacto.objects.filter(fuente=request.user,fecha_aceptacion=None ,original=True)
    amigos=[]
    for i in contactos:
        amigo=i.destino
        al=Album.objects.get(usuario=amigo,tipo='P')
        try:
            foto=Foto.objects.get(album=al,tipo='P')
        except:
            foto=1
        a={
            'contacto':i,
            'foto':foto
        }
        amigos.append(a)


    return amigos

def get_numero_aceptacion_no_vista(request):
    contactos=Contacto.objects.filter(destino=request.user,fecha_aceptacion=None,original=True , visto=False)
    return contactos.count()

def get_numero_mensajes_no_visto(request):
    mensajes=Mensaje.objects.filter(para=request.user.usuario,visto=False)
    return mensajes.count()




