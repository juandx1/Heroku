$(function(){

    $(window).scroll(function(){

        if($(window).scrollTop() + $(window).height() == $(document).height()){
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
    $('#coment_form','.comentar').submit(function(e) {

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


function mensajeSuccess(data, textStatus, jqXHR)
{
     $('#mensaje').html(data);
}


function comentSuccess(data, textStatus, jqXHR)
{
   $(this).closest("article[id]").find(".comentarios").append(data)
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
