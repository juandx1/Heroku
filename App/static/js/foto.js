function cargarFotoSizer() {
    var foto = $('#foto');

    if (foto.width() > foto.height()) {
        foto.addClass("foto-ancho");
        var div_foto = $('.div-foto').removeClass('div-foto');
    }
    else {
        foto.addClass("foto-alto");
    }
}