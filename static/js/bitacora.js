$(document).ready(function () {

    $(".comentarr").hide()

    $(".mostrar").click(function (e) { 
        e.preventDefault();
        seccion = $(this).data('btnsect')
        $(".comentarr").each(function () { 
           posicionn =  $(this).data("seccion")
           if (seccion == posicionn) {
            if ($(this).is(":visible")) {
                $(this).hide();
            } else {
                $(".comentarr").hide();
                $(this).show();
            }
           }
        });
    });

});