$(document).ready(function () {
    $("#hdrctn").hide()

    $("#secciones").click(function () { 
        $("#hdrctn").slideToggle();
    });

    $("#btnLog").click(function () { 
        window.location.href = "../../logout"
    });

    $("#home").click(function () { 
        window.location.href = "/User_v/menu.html"
    });

    //Carrito
    $("#carrito_h").hide()
    $("#btncar").click(function (e) { 
        e.preventDefault();
        alert("Ya se encuentra en la vista del carro")
    });
});