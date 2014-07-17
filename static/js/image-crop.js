    $('.foto-amigo').each(function(i){
        var alto = $(this).height();
        var ancho = $(this).width();

        if(alto>ancho){
            $(this).addClass('img-alto')
        }else{
            $(this).addClass('img-ancho')
        }
    })

    $('.ultima-foto').each(function(i){
        var alto = $(this).height();
        var ancho = $(this).width();

        if(alto>ancho){
            $(this).addClass('img-alto')
        }else{
            $(this).addClass('img-ancho')
        }
    })

    $('.img-avatar').each(function(i){
        var alto = $(this).height();
        var ancho = $(this).width();

        if(alto>ancho){
            $(this).addClass('img-alto')
        }else{
            $(this).addClass('img-ancho')
        }
    })