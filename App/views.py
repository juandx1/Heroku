from django.conf import settings
from django.shortcuts import render
from App.forms import UserForm, UserProfileForm, ImagenForm, AlbumForm, PostForm, ComentarioForm, ImageUploadForm
from App.models import *
from django.core.mail import send_mail
from django.shortcuts import render_to_response,get_object_or_404, render
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from App.functions import *
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import hashlib



#Modulo Registro
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/perfil/')
            else:
                return render(request,'login.html', {'fallo':2})
        else:
            return render(request,'login.html', {'fallo':1})
    else:
        return render(request,'login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/home')

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.username=user.email
            user.is_active = False
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            subject = "Gracias por Registarse a nustra red social cristiana DITAM te ama"
            var1 = str(user.email)+str(user.pk)+"ditam"
            var1 = var1.encode('utf-8')
            var2 = hashlib.md5(var1)
            var2 = var2.hexdigest()
            message = "Para confirmar su cuenta con la red DITAM haga click en el siguiente enlace: http://192.168.1.102:8000/confirmacion?hash="+str(var2)+"&token="+str(user.pk)+""

            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email, settings.EMAIL_HOST_USER]
            send_mail(subject,message,from_email,to_list,fail_silently=False);
            registered = True
            return render(request,'registroCompleto.html',{})

        else:
            pass
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def home(request):
    return render(request,'index.html',{})

def confirmacion(request):
    if request.method == 'GET':
        confirmacion = request.GET['hash']
        usuario= request.GET['token']
        user = User.objects.get(pk=usuario)
        var1 = str(user.email)+str(user.pk)+"ditam"
        var1 = var1.encode('utf-8')
        var2 = hashlib.md5(var1)
        var2 = var2.hexdigest()
        if str(var2) == str(confirmacion):
            user.is_active = True
            user.save()
            return render(request,'confirmacionCorrecto.html',{})
        else:
            raise Http404



#modulo Perfil
@login_required
def perfil(request):
    template = "perfil.html"
    if request.user.is_active:

        #obteniendo imagen de perfil y cover

        cover=get_imagen_cover(request.user)
        perfil=get_imagen_perfil(request.user)

        #obteniendo lista de post
        listaPosts =  get_lista_posts(request.user)

        #obteniendo lista de fotos
        albumes=Album.objects.filter(usuario=request.user)
        fotos=[]
        for i in albumes:
            if Foto.objects.filter(album=i).exclude(tipo='C').count()>0:
                for j in Foto.objects.filter(album=i).exclude(tipo='C'):
                    fotos.append(j)
            if len(fotos)==4:
                break

        #obteniendo lista de amigos
        lista=Contacto.objects.filter(fuente=request.user).exclude(fecha_aceptacion=None)[:9]
        amigos=[]
        for amigo in lista:
            try:
                al=Album.objects.get(usuario=amigo.destino,tipo='P')
                foto=Foto.objects.get(album=al,tipo='P')
            except:
                foto=1
            a={
                'foto': foto,
                'amigo':amigo.destino,
            }
            amigos.append(a)




        post_form=PostForm(initial={'user':request.user.pk})

        peticiones_amistad=get_numero_aceptacion_no_vista(request)
        mensajes_no_vistos=get_numero_mensajes_no_visto(request)

        return render(request, template,{'foto_perfil':perfil, 'foto_cover':cover,'lista':listaPosts,'post_form':post_form ,'fotos':fotos ,'amigos':amigos, 'usuario':request.user.pk ,'peticiones_amistad':peticiones_amistad ,'mensajes_no_vistos':mensajes_no_vistos})

    else:
        return render(request, template,{'foto_perfil':1, 'foto_cover':1})

@login_required
def nuevo_comentario(request):
   context = RequestContext(request)

   if request.method == 'POST':
        comentario_form=ComentarioForm(request.POST)
        if comentario_form.is_valid():
            nuevocomentario=comentario_form.save(commit=False)
            id=comentario_form.cleaned_data['id']
            post=Post.objects.get(pk=id)
            nuevocomentario.post=post
            nuevocomentario.usuario=request.user
            nuevocomentario.save()
            try:
                al=Album.objects.get(usuario=nuevocomentario.usuario,tipo='P')
                foto=Foto.objects.get(album=al,tipo='P')
            except:
                foto=1

            return render_to_response('ajax_comentario.html',{'comentario':nuevocomentario,'foto':foto})
@login_required
def nuevo_post(request):
   if request.method == 'POST':
        post_form=PostForm(request.POST)
        if post_form.is_valid():
            usuario=post_form.cleaned_data['user']
            nuevopost=post_form.save(commit=False)
            nuevopost.destino=User.objects.get(pk=usuario)
            nuevopost.fuente=request.user
            nuevopost.save()


            listaPosts = []
            posts=[]
            posts.append(nuevopost)

            user=User.objects.get(pk=usuario)
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

            if user==request.user:
                template='ajax_nuevo_post_usuario.html'
            else:
                template='ajax_nuevo_post.html'



            return render(request, template,{'lista':listaPosts})

@login_required
def eliminar_post(request,post_id):
    post=Post.objects.get(pk=post_id)

    if post.destino==request.user:
        post.delete()
    elif post.fuente == request.user:
        post.delete()
    else:
        raise  Http404
    return HttpResponseRedirect("/")

@login_required
def eliminar_comentario(request,comentario_id):
    comentario=Comentario.objects.get(pk=comentario_id)

    if comentario.post.destino==request.user:
        comentario.delete()
    elif comentario.usuario == request.user:
        comentario.delete()
    else:
        raise  Http404
    return HttpResponseRedirect("/")

@login_required
def usuario_amigo(request , user):
    template = "perfil_amigo.html"
    if request.user.is_active:

        #obteniendo inmagen de perfil y cover
        cover=get_imagen_cover(user)
        perfil=get_imagen_perfil(user)

        #obteniendo lista de post
        listaPosts =  get_lista_posts(user)

        #obteniendo lista de fotos
        albumes=Album.objects.filter(usuario=user)
        fotos=[]
        for i in albumes:
            if Foto.objects.filter(album=i).exclude(tipo='C').count()>0:
                for j in Foto.objects.filter(album=i).exclude(tipo='C'):
                    fotos.append(j)
            if len(fotos)==4:
                break

        #obteniendo lista de amigos
        lista=Contacto.objects.filter(fuente=user).exclude(fecha_aceptacion=None)[:9]
        amigos=[]
        for amigo in lista:
            try:
                al=Album.objects.get(usuario=amigo.destino,tipo='P')
                foto=Foto.objects.get(album=al,tipo='P')
            except:
                foto=1


            a={
                'foto': foto,
                'amigo':amigo.destino,
            }
            amigos.append(a)




        post_form=PostForm(initial={'user': user.pk})

        return render(request, template,{'foto_perfil':perfil, 'foto_cover':cover,'lista':listaPosts,'post_form':post_form ,'fotos':fotos ,'amigos':amigos, 'usuario':user})

    else:
        return render(request, template,{'foto_perfil':1, 'foto_cover':1})

@login_required
def ajax_post(request):
    if request.method=="GET":
        page=request.GET['page']
        user=request.GET['usuario']
    else:
        page=1
        user=request.user

    #obteniendo lista de post
    user=User.objects.get(pk=user)
    listaPosts =  get_lista_posts_ajax(user,page)
    return render_to_response('ajax_post.html',{'lista':listaPosts})

@login_required
def ver_usuario(request, usuario_id):

    amigo=Usuario.objects.get(pk=usuario_id)

    try:
        contacto =Contacto.objects.get(fuente=request.user.usuario,destino=amigo)
        if contacto.fecha_aceptacion==None:
            pass
        else:
           return  usuario_amigo(request , contacto.destino)
    except:
        if amigo.user.pk==request.user.pk:
            return perfil(request)

    return HttpResponse('')


#Modulo Fotos
@login_required
def subir_foto_album(request):
    if request.method == 'POST':
        form=ImagenForm(request.POST,request.FILES)
        if form.is_valid():
            album_id=request.POST['album']
            album=Album.objects.get(pk=album_id)
            foto=form.save(commit=False)
            foto.tipo='N'
            foto.album=album
            foto.save()

            return HttpResponseRedirect("/foto/"+ str(foto.pk))
    raise Http404

def crear_album(request):
    if request.method == 'POST':
        form=AlbumForm(request.POST)
        if form.is_valid():
            album=form.save(commit=False)
            album.tipo='N'
            album.usuario=request.user.usuario
            album.save()

            return HttpResponseRedirect("/album/"+str(album.pk))
    else:
        form=AlbumForm()

    template="crearAlbum.html"
    return render_to_response(template,context_instance=RequestContext(request, locals()))

@login_required
def albumes(request,user_id):

    user=User.objects.get(pk=user_id)
    cover=get_imagen_cover(user)
    perfil=get_imagen_perfil(user)

    print(cover)
    listaAlbumes = get_lista_albumes(user)
    form=AlbumForm()
    Albumes={'Albumes':listaAlbumes,'foto_perfil':perfil,'foto_cover':cover,'form':form}
    template="albumes.html"

    return render(request,template,Albumes)

@login_required
def editar_Foto(request,foto_id):

    foto=Foto.objects.get(pk=foto_id)
    fotos=Foto.objects.filter(album=foto.album)
    paginator = Paginator(fotos, 1) # muestra 1 foto por pagina


    page = request.GET.get('page')
    try:
        fotos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        a=1
        for i in fotos:
            if i==foto:
                break
            a=a+1
        print(a)
        fotos = paginator.page(a)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        fotos = paginator.page(paginator.num_pages)



    if foto.album.usuario.user!=request.user:
        raise  Http404
    template = "foto.html"
    return render(request, template,{'foto':foto,'paginator':fotos})

@login_required
def editar_album(request,album_id):
    listaFotos = []
    album=Album.objects.get(pk=album_id)
    cover=get_imagen_cover(request.user)
    perfil=get_imagen_perfil(request.user)

    for j in Foto.objects.filter(album=album):
        a={
          'foto':j,
          }
        listaFotos.append(a)

    lista={'fotos':listaFotos,'album':album}
    template="album.html"
    form=ImagenForm(initial={'album':album})


    return render(request,template,{'lista':lista,'foto_perfil':perfil,'foto_cover':cover ,'form':form})

@login_required
def eliminar_Foto(request,foto_id):
    foto=Foto.objects.get(pk=foto_id)
    if foto.album.usuario.user!=request.user:
        raise  Http404
    foto.delete()

    template="/album/"+str(foto.album.pk)
    return HttpResponseRedirect(template)

@login_required
def eliminar_album(request,album_id):
    album=Album.objects.get(pk=album_id)
    if album.tipo=='P' or album.tipo=='O' or album.tipo=='C' :
        raise Http404
    if album.usuario.user!=request.user:
        raise  Http404
    album.delete()
    template="/albumes/"+ str(request.user.pk)
    return HttpResponseRedirect(template)

@login_required
def fotos(request):
    listaAlbumes = []
    albumes=Album.objects.filter(usuario=request.user.usuario)
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
    Albumes={'Albumes':listaAlbumes}
    template="fotos.html"
    return render(request,template,Albumes)

@login_required
def perfil_foto(request,foto_id):
    al=Album.objects.get(usuario=request.user.usuario , tipo='P')
    foto=Foto.objects.filter(album=al , tipo='P')
    if foto.count()>0:
        foto=foto[0]
        foto.tipo='N'
        foto.save()
    nuevafoto=Foto.objects.get(pk=foto_id)
    nuevafoto.tipo='P'
    nuevafoto.album=al
    nuevafoto.save()
    template="/album/" + str(al.pk)
    return HttpResponseRedirect(template)

@login_required
def cover_foto(request,foto_id):
    al=Album.objects.get(usuario=request.user.usuario , tipo='C')
    foto=Foto.objects.filter(album=al , tipo='C')
    if foto.count()>0:
        foto=foto[0]
        foto.tipo='N'
        foto.save()
    nuevafoto=Foto.objects.get(pk=foto_id)
    nuevafoto.tipo='C'
    nuevafoto.album=al
    nuevafoto.save()
    template="/album/" + str(al.pk)
    return HttpResponseRedirect(template)

def ver_albumes(request,user_id):
   user=User.objects.get(pk=user_id)
   cover=get_imagen_cover(user)
   perfil=get_imagen_perfil(user)

   listaAlbumes = get_lista_albumes(user)
   Albumes={'Albumes':listaAlbumes,'foto_perfil':perfil,'foto_cover':cover,'usuario':user.usuario}
   template="albumes_amigo.html"

   return render(request,template,Albumes)

def ver_album(request,user_id,album_id):
   user=User.objects.get(pk=user_id)
   listaFotos = []
   album=Album.objects.get(pk=album_id)
   cover=get_imagen_cover(user)
   perfil=get_imagen_perfil(user)

   for j in Foto.objects.filter(album=album):
       a={
         'foto':j,
         }
       listaFotos.append(a)
   lista={'fotos':listaFotos,'album':album}
   template="album_amigo.html"


   return render(request,template,{'lista':lista,'foto_perfil':perfil,'foto_cover':cover,'usuario':user.usuario })

def ver_foto(request,foto_id):



    foto=Foto.objects.get(pk=foto_id)
    fotos=Foto.objects.filter(album=foto.album)
    paginator = Paginator(fotos, 1) # muestra 1 foto por pagina
    usuario=foto.album.usuario.user

    page = request.GET.get('page')
    try:
        fotos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        a=1
        for i in fotos:
            if i==foto:
                break
            a=a+1
        print(a)
        fotos = paginator.page(a)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        fotos = paginator.page(paginator.num_pages)

    template = "foto_amigo.html"
    return render(request, template,{'foto':foto,'paginator':fotos ,'usuario':usuario } )

#Modulo Amigos
@login_required
def ajax_amigos(request):
    busqueda=request.GET['busqueda']
    contactos=Contacto.objects.filter(fuente=request.user).exclude(fecha_aceptacion=None)
    lista=[]
    if len(busqueda)>0:
        lista=contactos.filter( Q(destino__user__first_name__contains=busqueda)| Q(destino__user__last_name__contains=busqueda))
    else:
        lista=contactos
    amigos=[]
    for i in lista:
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

    izquierda=[]
    derecha=[]
    izq=False
    for i,contacto in enumerate(amigos):
        if i%1==0:
            izq= not izq
        if izq:
            izquierda.append(contacto)
        else:
            derecha.append(contacto)



    template="ajax_amigos.html"
    return render(request,template,{'izquierda': izquierda, 'derecha':derecha })

@login_required
def ajax_ver_amigos(request):
    busqueda=request.GET['busqueda']
    user=request.GET['usuario']
    contactos=Contacto.objects.filter(fuente=user).exclude(fecha_aceptacion=None)
    lista=[]
    if len(busqueda)>0:
        lista=contactos.filter( Q(destino__user__first_name__contains=busqueda)| Q(destino__user__last_name__contains=busqueda))
    else:
        lista=contactos
    amigos=[]
    for i in lista:
        amigo=i.destino
        al=Album.objects.get(usuario=amigo,tipo='P')
        try:
            foto=Foto.objects.get(album=al,tipo='P')
        except:
            foto=1

        try:
            Contacto.objects.get(fuente=request.user, destino=i.destino)
            amigo=1
        except:
            if request.user == i.destino.user:
                amigo=3
            else:
                amigo=2
        a={
            'contacto':i,
            'foto':foto,
            'amigo':amigo
        }
        amigos.append(a)

    izquierda=[]
    derecha=[]
    izq=False
    for i,contacto in enumerate(amigos):
        if i%1==0:
            izq= not izq
        if izq:
            izquierda.append(contacto)
        else:
            derecha.append(contacto)



    template="ajax_ver_amigos.html"
    return render(request,template,{'izquierda': izquierda, 'derecha':derecha })

@login_required
def amigos(request):

    contactos=Contacto.objects.filter(fuente=request.user).exclude(fecha_aceptacion=None)
    contactos.order_by('fuente__first_name')

    try:
        al = Album.objects.get(usuario=request.user.usuario, tipo='C')
        cover = Foto.objects.get(album=al, tipo='C')
    except:
        cover = 1
    try:
        al = Album.objects.get(usuario=request.user.usuario, tipo='P')
        perfil = Foto.objects.get(album=al, tipo='P')
    except:
        perfil = 1

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

    izquierda=[]
    derecha=[]
    izq=False
    for i,contacto in enumerate(amigos):
        if i%1==0:
            izq= not izq
        if izq:
            izquierda.append(contacto)
        else:
            derecha.append(contacto)


    template="amigos.html"
    return render(request,template,{'contactos':contactos,'izquierda': izquierda, 'derecha':derecha ,'foto_perfil': perfil, 'foto_cover': cover })

@login_required
def ver_amigos(request,amigo_id):

    user=User.objects.get(pk=amigo_id)
    contactos=Contacto.objects.filter(fuente=user).exclude(fecha_aceptacion=None)
    contactos.order_by('fuente__first_name')

    amigos=[]
    for i in contactos:
        amigo=i.destino
        al=Album.objects.get(usuario=amigo,tipo='P')
        try:
            foto=Foto.objects.get(album=al,tipo='P')
        except:
            foto=1

        try:
            Contacto.objects.get(fuente=request.user, destino=i.destino)
            amigo=1
        except:
            if request.user == i.destino.user:
                amigo=3
            else:
                amigo=2

        a={
            'contacto':i,
            'foto':foto,
            'amigo':amigo
        }
        amigos.append(a)

    izquierda=[]
    derecha=[]
    izq=False
    for i,contacto in enumerate(amigos):
        if i%1==0:
            izq= not izq
        if izq:
            izquierda.append(contacto)
        else:
            derecha.append(contacto)


    template="ver_amigos.html"
    return render(request,template,{'izquierda': izquierda, 'derecha':derecha ,'usuario':user })



#Solicitudes de amistada que aun no han sido aceptadas por el usuario actual
@login_required
def solicitud_pendiente(request):
    contactos=Contacto.objects.filter(destino=request.user,fecha_aceptacion=None,original=True)
    contactos.order_by('fuente__first_name')
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

    izquierda=[]
    derecha=[]
    izq=False
    for i,contacto in enumerate(amigos):
        if i%1==0:
            izq= not izq
        if izq:
            izquierda.append(contacto)
        else:
            derecha.append(contacto)
    template="solicitud_pendiente.html"
    return render(request,template,{'izquierda': izquierda, 'derecha':derecha })


#Solicitudes de amistades que aun no han sido respondida por los usuarios destino
@login_required
def invitacion_pendiente(request):
    contactos=Contacto.objects.filter(fuente=request.user,fecha_aceptacion=None ,original=True)
    contactos.order_by('fuente__first_name')
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

    izquierda=[]
    derecha=[]
    izq=False
    for i,contacto in enumerate(amigos):
        if i%1==0:
            izq= not izq
        if izq:
            izquierda.append(contacto)
        else:
            derecha.append(contacto)
    template="invitacion_pendiente.html"
    return render(request,template,{'izquierda': izquierda, 'derecha':derecha })

def eliminar_contacto(request, contacto_id):
    contacto=Contacto.objects.get(pk=contacto_id)
    contacto2=Contacto.objects.get(fuente=contacto.destino,destino=contacto.fuente)
    contacto.delete()
    contacto2.delete()
    template="/amigos"
    return HttpResponseRedirect(template)

@login_required
def eliminar_amigo(request, amigo_id):
    amigo=Usuario.objects.get(pk=amigo_id)
    contacto1=Contacto.objects.get(fuente=request.user,destino=amigo)
    contacto2=Contacto.objects.get(destino=request.user,fuente=amigo)
    contacto1.delete()
    contacto2.delete()
    template="/home"
    return HttpResponseRedirect(template)

@login_required
def agregar_amigo(request, amigo_id):
    amigo=Usuario.objects.get(pk=amigo_id)
    Contacto.objects.create(fuente=request.user.usuario,destino=amigo)
    template="/home"
    return HttpResponseRedirect(template)

@login_required
def aceptar_amigo(request, amigo_id):
    amigo=Usuario.objects.get(pk=amigo_id)
    contacto =Contacto.objects.get(fuente=request.user.usuario,destino=amigo)
    contacto.fecha_aceptacion=datetime.now()
    contacto.save()
    template="/home"
    return HttpResponseRedirect(template)

@login_required
def editar_Foto(request,foto_id):

    foto=Foto.objects.get(pk=foto_id)
    fotos=Foto.objects.filter(album=foto.album)
    paginator = Paginator(fotos, 1) # muestra 1 foto por pagina


    page = request.GET.get('page')
    try:
        fotos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        a=1
        for i in fotos:
            if i==foto:
                break
            a=a+1

        fotos = paginator.page(a)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        fotos = paginator.page(paginator.num_pages)



    if foto.album.usuario.user!=request.user:
        raise  Http404
    template = "foto.html"
    return render(request, template,{'foto':foto,'paginator':fotos})




#modulo mensajes
@login_required
def mensajes(request):
    mensajes=Mensaje.objects.filter(para=request.user.usuario).order_by('-fecha_envio')
    paginator = Paginator(mensajes, 10)

    if request.method=="GET":
        try:
            page=request.GET['page']
        except MultiValueDictKeyError:
            page=1

    try:
        mensajes = paginator.page(page)
    except PageNotAnInteger:
        mensajes = paginator.page(1)

    except EmptyPage:
        mensajes = paginator.page(paginator.num_pages)



    lista=[]
    if len(mensajes)>0:
        mensaje=mensajes[0]
        mensaje.visto=True
        mensaje.save()

    for i in mensajes:
        try:
            al=Album.objects.get(usuario=i.de,tipo='P')
            foto=Foto.objects.get(album=al,tipo='P')
        except:
            foto=1
        a={
            'mensaje':i,
            'foto':foto
        }
        lista.append(a)

    template="mensajes.html"
    return render(request,template,{'mensajes':lista, 'paginator':mensajes })

@login_required
def mensaje(request,mensaje_id):
    mensaje=Mensaje.objects.get(pk=mensaje_id)
    mensaje.visto=True
    mensaje.save()

    return render_to_response('ajax_mensaje.html',{'mensaje':mensaje})

@login_required
def eliminar_mensaje(request,mensaje_id):
    mensaje=Mensaje.objects.get(pk=mensaje_id)
    if mensaje.para.user!=request.user:
        raise  Http404
    mensaje.delete()
    template="/mensajes"
    return HttpResponseRedirect(template)

@login_required
def nuevo_mensaje(request):
    template="nuevo_mensaje.html"
    return render(request,template,{})

@login_required
def ajax_destinatarios(request):
    busqueda=request.GET['busqueda']
    contactos=Contacto.objects.filter(fuente=request.user).exclude(fecha_aceptacion=None)
    lista=[]
    if len(busqueda)>0:
        lista=contactos.filter( Q(destino__user__first_name__contains=busqueda)| Q(destino__user__last_name__contains=busqueda))
    destinatarios=[]
    for i in lista:
        foto=get_imagen_perfil(i.destino)
        a={
            'destinatario':i.destino.user,
            'foto':foto
        }
        destinatarios.append(a)

    template="ajax_destinatarios.html"
    return render(request,template,{'lista':destinatarios})

def ajax_destinatario(request, destinatario_id):
    destinatario=User.objects.get(pk=destinatario_id)
    template="ajax_destinatario.html"
    return render(request,template,{'destinatario':destinatario})

@login_required
def enviar_mensaje(request):
    lista=request.POST.getlist('destinatario')
    contenido=request.POST['mensaje']
    asunto=request.POST['asunto']

    for i in lista:
        mensaje=Mensaje.objects.create(de=request.user.usuario , para=Usuario.objects.get(pk=i) , contenido=contenido , asunto=asunto )

    return HttpResponseRedirect("/enviados")

@login_required
def enviados(request):
    mensajes=Mensaje.objects.filter(de=request.user.usuario).order_by('-fecha_envio')
    paginator = Paginator(mensajes, 10)

    if request.method=="GET":
        try:
            page=request.GET['page']
        except MultiValueDictKeyError:
            page=1

    try:
        mensajes = paginator.page(page)
    except PageNotAnInteger:
        mensajes = paginator.page(1)

    except EmptyPage:
        mensajes = paginator.page(paginator.num_pages)

    lista=[]
    if len(mensajes)>0:
        mensaje=mensajes[0]
        mensaje.visto=True
        mensaje.save()
    for i in mensajes:
        try:
            al=Album.objects.get(usuario=i.para,tipo='P')
            foto=Foto.objects.get(album=al,tipo='P')
        except:
            foto=1
        a={
            'mensaje':i,
            'foto':foto
        }
        lista.append(a)

    template="enviados.html"
    return render(request,template,{'mensajes':lista, 'paginator':mensajes })



#Modulo eventos
def eventos(request):

    eventos=Evento.objects.filter(usuario=request.user)
    cover=get_imagen_cover(request.user)
    perfil=get_imagen_perfil(request.user)
    template="eventos.html"
    return render(request,template,{'foto_perfil':perfil, 'foto_cover':cover ,'eventos':eventos})

def eventos_asistidos(request):

    invitaciones=Invitacion.objects.filter(usuario=request.user , evento__fecha_inicio__lt=datetime.now()).exclude(fecha_aceptacion=None)

    eventos=[]
    for i in invitaciones:
        eventos.append(i.evento)
    cover=get_imagen_cover(request.user)
    perfil=get_imagen_perfil(request.user)
    template="eventos.html"
    return render(request,template,{'foto_perfil':perfil, 'foto_cover':cover ,'eventos':eventos})

def eventos_pendientes(request):

    invitaciones=Invitacion.objects.filter(usuario=request.user , fecha_aceptacion=None )

    eventos=[]
    for i in invitaciones:
        eventos.append(i.evento)
    cover=get_imagen_cover(request.user)
    perfil=get_imagen_perfil(request.user)
    template="eventos.html"
    return render(request,template,{'foto_perfil':perfil, 'foto_cover':cover ,'eventos':eventos})

def editar_evento(request , evento_id ):
    if (request.method=='POST'):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            foto_perfil= form.cleaned_data['foto_perfil']
            foto_cover= form.cleaned_data['foto_cover']
            lugar = request.POST['lugar']
            fecha_inicio = request.POST['fecha_inicio']
            fecha_fin = request.POST['fecha_inicio']

    evento=Evento.objects.get(pk=evento_id)
    cover=get_imagen_cover(request.user)
    perfil=get_imagen_perfil(request.user)
    template="editarEvento.html"
    return render(request,template,{'foto_perfil':perfil, 'foto_cover':cover ,'evento':evento})

def crear_evento(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():

            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            foto_perfil= form.cleaned_data['foto_perfil']
            foto_cover= form.cleaned_data['foto_cover']
            lugar = request.POST['lugar']
            fecha_inicio = request.POST['fecha_inicio']
            fecha_fin = request.POST['fecha_inicio']

            lista=request.POST.getlist('destinatario')

            evento=Evento.objects.create(
                nombre=nombre,
                direccion=lugar,
                fecha_inicio=datetime.now(),
                fecha_fin=datetime.now(),
                descripcion=descripcion,
                usuario=request.user,
                foto_perfil=foto_perfil,
                foto_cover=foto_cover
            )


            for i in lista:
                Invitacion.objects.create(
                    fecha_invitacion=datetime.now(),
                    fecha_aceptacion=datetime.now(),
                    usuario=User.objects.get(pk=i),
                    evento=evento
                )

            return eventos(request)

        cover=get_imagen_cover(request.user)
        perfil=get_imagen_perfil(request.user)
        template="crearEvento.html"
        return render(request,template,{'foto_perfil':perfil, 'foto_cover':cover })

    cover=get_imagen_cover(request.user)
    perfil=get_imagen_perfil(request.user)
    template="crearEvento.html"
    return render(request,template,{'foto_perfil':perfil, 'foto_cover':cover })

