from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Iglesia(models.Model):
    direccion=models.CharField(max_length=100)
    nombre=models.CharField(max_length=140)
    telefono=models.IntegerField(max_length=15)
    url=models.URLField(blank=True)
    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    GENERO = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )

    user=models.OneToOneField(User)
    fecha_nacimiento=models.DateField()
    genero=models.CharField(max_length=1, choices=GENERO)
    pais=models.CharField(max_length=100)
    telefono=models.IntegerField(blank=True , max_length=15)
    iglesia=models.ForeignKey(Iglesia)
    contactos = models.ManyToManyField('self', symmetrical=False ,through='Contacto',  related_name='related_to+' )
    mensajes = models.ManyToManyField('self', symmetrical=False ,through='Mensaje',  related_name='Mensaje_de+' )
    def __str__(self):
        return self.user.username


class Album(models.Model):
    nombre=models.CharField(max_length=60)
    descripcion=models.CharField(blank=True,max_length=600)
    usuario=models.ForeignKey(Usuario)
    TIPO = (
        ('P', 'Perfil'),
        ('O', 'Otros'),
        ('N', 'Normal'),
        ('C', 'Cover'),
    )
    tipo=models.CharField(max_length=1, choices=TIPO)
    def __str__(self):
        return self.nombre

class Foto(models.Model):
    album=models.ForeignKey(Album)
    imagen=models.ImageField(upload_to='profile/')
    TIPO = (
        ('P', 'Perfil'),
        ('C', 'Cover'),
        ('N', 'Normal'),
    )
    tipo=models.CharField(max_length=1, choices=TIPO)




class Post(models.Model):
    contenido=models.CharField(max_length=600)
    fuente=models.ForeignKey(User, related_name='fuente')
    destino=models.ForeignKey(User, related_name='destino')
    fecha_publicacion=models.DateTimeField(auto_now_add=True)


class Comentario(models.Model):
    contenido=models.CharField(max_length=600)
    usuario=models.ForeignKey(User)
    post=models.ForeignKey(Post)
    fecha_publicacion=models.DateTimeField(auto_now_add=True)
    visto=models.BooleanField(default=False)

class Evento(models.Model):
    nombre=models.CharField(max_length=100)
    direccion=models.CharField(max_length=100)
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    descripcion=models.CharField(max_length=600 ,blank=True)
    usuario=models.ForeignKey(User)
    foto_perfil=models.ImageField(upload_to='eventos/')
    foto_cover=models.ImageField(upload_to='eventos/')


class Invitacion(models.Model):
    fecha_invitacion=models.DateField()
    fecha_aceptacion=models.DateField(null=True, blank=True)
    usuario=models.ForeignKey(User)
    evento=models.ForeignKey(Evento)
    visto=models.BooleanField(default=False)

class Contacto(models.Model):
    fuente=models.ForeignKey(Usuario, related_name='fuente')
    destino=models.ForeignKey(Usuario, related_name='destino')
    original=visto=models.BooleanField(default=True)
    fecha_invitacion=models.DateField(auto_now_add=True)
    fecha_aceptacion=models.DateField(null=True, blank=True)
    visto=models.BooleanField(default=False)

class Mensaje(models.Model):
    de=models.ForeignKey(Usuario, related_name='de')
    para=models.ForeignKey(Usuario, related_name='para')
    fecha_envio=models.DateTimeField(auto_now_add=True)
    asunto=models.CharField(max_length=140,blank=True)
    contenido=models.CharField(max_length=600)
    visto=models.BooleanField(default=False)



def do_something(sender, **kwargs):
    obj = kwargs['instance']
    post_save.disconnect(do_something, sender=Contacto)

    try:
        contacto=Contacto.objects.get(fuente=obj.destino, destino=obj.fuente)
        contacto.fecha_aceptacion=obj.fecha_aceptacion
        contacto.save()
    except:
        contacto_nuevo=Contacto.objects.create(
            fuente=obj.destino,
            destino=obj.fuente,
            fecha_invitacion=obj.fecha_invitacion,
            fecha_aceptacion=obj.fecha_aceptacion,
            original=False,
        )


    post_save.connect(do_something, sender=Contacto)

def do_something2(sender, **kwargs):
    obj = kwargs['instance']

    if Album.objects.filter(usuario=obj).count()==0:
        album_perfil=Album.objects.create(
                nombre="Imagenes de perfil",
                descripcion="Aqui se guardan tus imagenes de perfil",
                usuario=obj,
                tipo='P'
        )
        album_perfil.save()

        album_otros=Album.objects.create(
                nombre="Imagenes sin album",
                descripcion="Aqui se guardan tus imagenes sin album",
                usuario=obj,
                tipo='O'
        )
        album_otros.save()

        album_cover=Album.objects.create(
                nombre="Imagenes del cover",
                descripcion="Aqui se guardan tus imagenes del cover",
                usuario=obj,
                tipo='C'
        )
        album_cover.save()





post_save.connect(do_something, sender=Contacto)
post_save.connect(do_something2, sender=Usuario)
