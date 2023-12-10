$(document).ready(function () {
    $('#carro').on('click', function() {
        var producto_id = $(this).val(); // Obtener el producto_id del botón que se hizo clic
        console.log (producto_id)
        $('#modalAgregarAlCarrito').modal('show');
    });

    $('#confirmarAgregar').on('click', function() {
        var cantidad = $('#cantidad').val();
        var producto_id = $('#carro').val(); // Obtener el producto_id guardado en el modal
        console.log('Producto ID:', producto_id);
        var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; 
    
        $.ajax({
            type: 'POST',
            url: '/agregar_al_carrito/', // Ruta correcta hacia la vista en Django
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            data: {
                'producto_id': producto_id,
                'cantidad': cantidad
            },
            success: function(response) {
                // Manejar la respuesta exitosa aquí
                console.log(response);
                $('#modalAgregarAlCarrito').modal('hide');
                alert ("Se ha añadido con exito")
                location.reload()
            },
            error: function(error) {
                // Manejar errores de la solicitud aquí
                console.error(error);
            }
        });
    });

    $("#publicar_c").click(function () { 
        comentario = $("#comentar1").val()
        user = $("#inptName").val()
        producto_id = $("#inptid").val()
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        $.ajax({
            type: "POST",
            url: "/Admin_v/ver_productos.html/" + producto_id + "/",
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            data: {
                'comentario' : comentario,
                'user' : user
            },
            success: function (response) {
                location.reload()
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });

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