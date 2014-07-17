function imageCrop() {

    $('.foto-album').each(function (i) {
        var alto = $(this).height();
        var ancho = $(this).width();

        if (alto > ancho) {
            $(this).addClass('img-alto')
        } else {
            $(this).addClass('img-ancho')
        }
    })

    $('.foto-amigo').each(function (i) {
        var alto = $(this).height();
        var ancho = $(this).width();

        if (alto > ancho) {
            $(this).addClass('img-alto')
        } else {
            $(this).addClass('img-ancho')
        }
    })

    $('.ultima-foto').each(function (i) {
        var alto = $(this).height();
        var ancho = $(this).width();

        if (alto > ancho) {
            $(this).addClass('img-alto')
        } else {
            $(this).addClass('img-ancho')
        }
    })

    $('.img-avatar').each(function (i) {
        var alto = $(this).height();
        var ancho = $(this).width();

        if (alto > ancho) {
            $(this).addClass('img-alto')
        } else {
            $(this).addClass('img-ancho')
        }
    })

    $('.foto-perfil').each(function (i) {
        var alto = $(this).height();
        var ancho = $(this).width();

        if (alto > ancho) {
            $(this).addClass('img-alto')
        } else {
            $(this).addClass('img-ancho')
        }
    })

    $('.avatar').each(function (i) {
        var alto = $(this).height();
        var ancho = $(this).width();

        if (alto > ancho) {
            $(this).addClass('img-alto')
        } else {
            $(this).addClass('img-ancho')
        }
    })

}