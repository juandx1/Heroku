__author__ = 'Alejandro'

from App.functions import get_lista_aceptacion_pendiente , get_numero_mensajes_no_visto

def notificaciones(request):
    if request.user.is_authenticated():
        aceptar_amistad=get_lista_aceptacion_pendiente(request)
        mensajes_no_visto=get_numero_mensajes_no_visto(request)
        return{ 'aceptar_amistad':len(aceptar_amistad), 'mensajes_no_visto':mensajes_no_visto }
    return {}