$(document).ready(function () {

    $("#ctn_fil").hide()

    $('#search').on('input', function() {
        var resultados = $(this).val();
        $("#ctn_fil").show();
        $("#result_fil").show();

        if (resultados === "") {
            $("#ctn_fil").hide();
            return;
        }

        $.ajax({
            type: 'GET',
            url: '/User_v/productos.html',
            data: {
                'search': resultados
            },
            success: function(response) {
                var productos_filtrado = response.filtered_products;
                var html = '';

                if (resultados != "") {
                    productos_filtrado.forEach(function(product) {
                        html += '<div style="display: flexbox;">';
                        html += '<a href="/User_v/ver_productos.html/' + product.id + '" style="font-size: 20px;" >' + product.name + '</a>' ;
                        html += '</div>';
                    });
                    $('#result_fil').show();
                    $('#result_fil').html(html);
                } else
                    $('#result_fil').hide();
            }
        });
    });


    $('.btnCar').on('click', function() {
        var producto_id = $(this).data('producto_id'); // Obtener el producto_id del botón que se hizo clic
        $('#modalAgregarAlCarrito').modal('show').data('producto_id', producto_id);
    });

    $('#confirmarAgregar').on('click', function() {
        var cantidad = $('#cantidad').val();
        var producto_id = $('#modalAgregarAlCarrito').data('producto_id'); // Obtener el producto_id guardado en el modal
        console.log('Producto ID:', producto_id);
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
                $('#modalAgregarAlCarrito').modal('hide');
                alert("Se ha añadido con exito")
                location.reload()
            },
            error: function(error) {
                console.error(error);
            }
        });
    });
});