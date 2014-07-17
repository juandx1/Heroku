$('.foto-animado')
    .mouseenter(function () {
        if (screen.width > 992) {
            $('.nombre').css("left", "0px");
        }
    })
    .mouseleave(function () {
        if (screen.width > 992) {
            $('.nombre').css("left", "100%");
        }
    });

if(screen.width < 992){
    $('#busqueda').removeClass("pull-right").addClass("pull-left");
}