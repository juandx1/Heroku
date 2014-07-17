$(function(){
    $(window).scroll(function(){
        console.log($(window).scrollTop() + $(window).height());
        console.log( $(document).height());

        if($(window).scrollTop() + $(window).height() +1 >= $(document).height()){
            console.log("popo");
           $.ajax({
            type: "GET",
            url: "/ajax/post/",
            data: {
                'page' : $('#page').val(),
                'usuario' : $('#usuario').val()
                /** 'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val() */
            },
            success: loadSuccess,
            dataType: 'html'
        });
        }
    });

});


$(function(){
    $('#cargar').click(function(){



           $.ajax({
            type: "GET",
            url: "/ajax/post/",
            data: {
                'page' : $('#page').val(),
                'usuario' : $('#usuario').val()
                /** 'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val() */
            },
            success: loadSuccess,
            dataType: 'html'
        });

    });

});

$(function(){
    $(document).on("submit",'#coment_form',function(e){

        $.ajax({ // create an AJAX call...
            context: this,
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: comentSuccess
        });
        e.preventDefault();
    });

});

$(function(){
    $('#user_form','.texto-comentario').submit(function(e) {
        $.ajax({ // create an AJAX call...
            context: this,
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: postSuccess
        });
        e.preventDefault();
    });

});

$(function(){
   $( "#destinatarios" ).keyup(function() {
        $.ajax({
            type: "GET",
            url: "/ajax/destinatarios/",
            data: {
                'busqueda' : $('#destinatarios').val()
                /** 'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val() */
            },
            success: destinatariosSuccess,
            dataType: 'html'
        });
    });

});




$(function(){
    $(".mensaje").click(function(e){
       $.ajax({ // create an AJAX call...

            type: "GET",
            url: $(this).attr('href'),
            data: { },
            success: mensajeSuccess
        });
        e.preventDefault();
    });
});

$(function(){
    $(document).on("click",'.destino',function(e){
        var txt=$(this).find("p").text();
        var a=$('#destinatarios_mensaje');
        var b=false;
        a.find("p").each(function() {

            if ( $(this).text()==txt)
               b=true;

        });
        if(!b){
             $.ajax({ // create an AJAX call...
                type: "GET",
                url: $(this).attr('href'),
                data: { },
                success: destinatarioSuccess
            });
        }
    e.preventDefault();
    });
});

$(function(){
    $(document).on("click",'.glyphicon.glyphicon-remove',function(e){
        $(this).parent().parent().remove()

    });

});

$(function(){
    $(document).on("click",'.rechazar',function(e){
        $(this).parent().parent().remove()
        $.ajax({ // create an AJAX call...
                type: "GET",
                url: $(this).attr('href'),
                data: { }

            });
        e.preventDefault();
    });

});

$(function(){
    $(document).on("click",'.aceptar',function(e){
        $(this).parent().parent().remove()
        $.ajax({ // create an AJAX call...
                type: "GET",
                url: $(this).attr('href'),
                data: { }

            });
        e.preventDefault();
    });

});




$(function(){
   $( "#amigos-busqueda" ).keyup(function() {

        $.ajax({
            type: "GET",
            url: "/ajax/amigos/",
            data: {
                'busqueda' : $('#amigos-busqueda').val()

                /** 'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val() */
            },
            success: amigosSuccess,
            dataType: 'html'
        });
    });

});

$(function(){
   $( "#ver_amigos" ).keyup(function() {
        $.ajax({
            type: "GET",
            url: "/ajax/ver/amigos/",
            data: {
                'busqueda' : $('#ver_amigos').val(),
                'usuario'  : $('#usuario').val()
                /** 'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val() */
            },
            success: amigosSuccess,
            dataType: 'html'
        });
    });

});



$(function(){
    $(document).on("click",'.eliminar-post',function(e){

        $.ajax({ // create an AJAX call...
                context: this,
                type: "GET",
                url: $(this).attr('href'),
                data: { },
                success: eliminarPostSuccess
            });
        e.preventDefault();
    });

});

$(function(){
    $(document).on("click",'.eliminar-comentario',function(e){

        $.ajax({ // create an AJAX call...
                context: this,
                type: "GET",
                url: $(this).attr('href'),
                data: { },
                success: eliminarComentarioSuccess
            });
        e.preventDefault();
    });

});

function eliminarPostSuccess(data, textStatus, jqXHR)
{
    $(this).parent().parent().parent().parent().parent().remove().fadeOut('slow');
}

function eliminarComentarioSuccess(data, textStatus, jqXHR)
{
    $(this).parent().parent().parent().parent().remove().fadeOut('slow');
}


function amigosSuccess(data, textStatus, jqXHR)
{

    $('#resultado_amigos').html(data);
}



function destinatarioSuccess(data, textStatus, jqXHR)
{
    var a=$('#destinatarios_mensaje').append(data);
}

function destinatariosSuccess(data, textStatus, jqXHR)
{
     $('#resultado').html(data);
}

function mensajeSuccess(data, textStatus, jqXHR)
{
     $('#mensaje').html(data);
}

function comentSuccess(data, textStatus, jqXHR)
{
   $(this).closest("article[id]").find(".comentarios").append(data);
    console.log("asdasdasda");
    var textarea = $('.texto-comentario-usuarios');
    textarea.val('');
}

function postSuccess(data, textStatus, jqXHR)
{
    $('#comentar_muro').after(data);
    $('.comentario').eq(1).hide().fadeIn(100);
    $('.estado').val('');
}

function loadSuccess(data, textStatus, jqXHR)
{
    $('#nuevo').append(data);
    $('#page').val(function(index,currentvalue){
        return +currentvalue + +1;
    })
}
/**
 * Created by Onatra on 26/06/14.
 */
