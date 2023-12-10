$(document).ready(function () {
//Registro exitoso
    var mensaje = $("#reg_ext").text()
        $("#reg_ext").hide()
        
            if (mensaje.trim() !== ""){
                $("#reg_ext").show()

                setTimeout(function() {
                    $("#reg_ext").fadeOut(500, function() {
                        window.location.href = "/"
                    });
                }, 3000);
            }
            
    $('#search_P').on('input', function() {
        var resultados = $(this).val();

        $.ajax({
            type: 'GET',
            url: '/Admin_v/menu.html',
            data: {
                'search_P': resultados
            },
            success: function(response) {
                var recetas_filtradas = response.filtrado;
                if (resultados != "") {
                    $('#Productos').show();
                    mostrarResultados(recetas_filtradas)
                } else
                    $('#Productos').hide();
            }
        });
    });

    function mostrarResultados(respuesta) {
        var html = '';
        for (var i = 0; i < respuesta.length; i++) {
            html += '<div>';
            html += '<a class="ml-2 mb-2" style="font-size: 19px" href="/Admin_v/ver_productos.html/' + respuesta[i].id + '">' + respuesta[i].name + '</a>';
        }
        $('#Productos').html(html);
        $('#Productos a').on('click', function(event) {
            event.preventDefault();
            var href = $(this).attr('href');
            window.location.href = href;
        });
    }

    function next_previus (indexx, controlador, controlador2, pro_re, index_stop){
        $('.slider_h').slice(5).hide();
        $('.slider_R').slice(4).hide();
        $(controlador).click(function() {
        const valor = $(pro_re);
            if (indexx < valor.length) {
                    valor.eq(indexx).show();
                    valor.eq(indexx - index_stop).hide();
                    indexx++;
                }
            });

        $(controlador2).click(function() {
        const valor = $(pro_re);
            if (indexx > index_stop) {
                    indexx--;
                    valor.eq(indexx).hide();
                    valor.eq(indexx - index_stop).show()
                }
            });
        }

    let index_P = 5;
    let index_R = 4

    next_previus (index_P, $("#next"), $("#prev"), $(".slider_h"), index_P)
    next_previus (index_R, $("#nextt"), $("#prevv"), $(".slider_R"), index_R)

    $(".carousel-item .Imgs_p").each(function(index) {
        let value = $('.lasimg').eq(index).val(); // Obtener el valor del input oculto
        $(this).attr('src', '../../../static/' + value); //Asignar ruta a cada imagen del carrusel
    });

    $('.btn-carro, .btn-carroo').on('click', function() {
        var producto_id = $(this).data('pro'); // Obtener el producto_id del botón que se hizo clic
        if (producto_id == '30' || producto_id == '31') {
            $('#modalAgregarAlCarrito').modal('show').data('pro', producto_id);
            $('.modal-body').hide()
        }
        $('#modalAgregarAlCarrito').modal('show').data('pro', producto_id);
    });
    
    $('#confirmarAgregar').on('click', function() {
        var cantidad = $('#cantidad').val();
        var producto_id = $('#modalAgregarAlCarrito').data('pro'); // Obtener el producto_id guardado en el modal
        var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
        $.ajax({
            type: 'POST',
            url: '/agregar_al_carrito/',
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
        
});
