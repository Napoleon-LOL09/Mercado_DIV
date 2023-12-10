$(document).ready(function() {
    var totalFinal = 0
    function subtotal() {
        var SubtotalF = 0;
            $('.producto').each(function() {
                var precio = $(this).data('precio');
                var cantidad = $(this).data('cantidad');
                var subtotal = precio * cantidad;
                SubtotalF += subtotal;
            });
        return SubtotalF
    }

    function calcularTotales() {
        var SubtotalF = 0;
        $('.producto').each(function() {
            var precio = $(this).data('precio');
            var cantidad = $(this).data('cantidad');
            var subtotal = precio * cantidad;
            SubtotalF += subtotal;

            totalFinal = SubtotalF + 0.00 + 0.50

            $(this).find('.subtotal').text(subtotal);
        });

        $('#subtotF').html('Subtotal' + '<label id=lblSut>' + SubtotalF + '$' + '</label>');
        $('#total').html('<label id="lblTap" class="mr-5"> Total a pagar </label>' + '<label>' + totalFinal + '</label>' +"$");
    }
    calcularTotales();

    $('.increment, .decrement, .remover').on('click', function(e) {
        e.preventDefault();
        var action = $(this).data('action');
        var row = $(this).closest('.producto');
        var productoId = row.data('id');
        var cantidad = row.data('cantidad');

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        if (action === 'increment') {
            cantidad++;
            row.data('cantidad', cantidad);
            row.find('.cantidad').text(cantidad);
            var precio = row.data('precio');
            var subtotal = precio * cantidad;
            
            row.find('.subtotal').text(subtotal);
            
            $('#subtotF').text('Subtotal: ' + subtotal);

            $.ajax({
                url: '/actualizar_cantidad/' + productoId + '/',
                type: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                data: { 'cantidad': cantidad }
             });
             calcularTotales();

        }else if(action === 'decrement') {
            if (cantidad > 1) {
                cantidad--;
                row.data('cantidad', cantidad);
                row.find('.cantidad').text(cantidad);
                var precio = row.data('precio');
                var subtotal = precio * cantidad;
                
                row.find('.subtotal').text(subtotal);
                
                $('#subtotF').text('Subtotal: ' + subtotal);

                $.ajax({
                    url: '/actualizar_cantidad/' + productoId + '/',
                    type: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken
                    },
                    data: 
                    {'cantidad': cantidad }
                });
                calcularTotales();
            }
        } else if (action === 'remove') {
            if (confirm("Seguro que deseas quitar este producto del carrito?")){
  
                $.ajax({
                    url: '/eliminar_del_carrito/' + productoId + '/',
                    type: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken
                    }, success: function () {  
                        row.remove();
                        calcularTotales();

                        if ($('.producto').length === 0) {
                            window.location.reload()
                        }
                    }
                });
                
            }
        }
    });

    var usado = 0;
    var limite = 0
    var fecha_fini = 0
    
    //Obtener Fecha de Hoy
    var fecha = new Date();
    var mes = fecha.getMonth() + 1
    var fecha_hoy = fecha.getFullYear() + '-' + mes + '-' + fecha.getDate();


    $("#veri_cup").submit(function (e) { 
        e.preventDefault();
        var SubtotalF = subtotal();
        const cod_cupon = $('#inpD').val().trim();
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        $.ajax({
            url: window.location.pathname,
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            } ,
            data: {
                'cod_cupon' : cod_cupon,
                'limite' : limite
            },
            success: function (response) {
                if (response.existe) {
                    descuento =  (SubtotalF * (response.descuento / 100))
                    calculoFinal = (SubtotalF - descuento);
                    redondeo = Math.round (calculoFinal * 100) / 100
                    alert ("Cupon con descuento del " + response.descuento +"%")
                    $("#cuponDes").html('Descuento ' + '<label style="font-weight: 100; margin-left: 136px;">' + descuento.toFixed(2) + '$' + '</label>')
                    $('#total').html('<label id="lblTap" class="mr-5"> Total a pagar </label>' + '<label>' + (redondeo + 0.50) + '</label>' +"$");
                    usado = response.usado
                    limite = response.limite
                    fecha_fini = response.fecha_f
                }
            },
            error: function () {
                alert ("Cupon Invalido")
            }
        });
    });


    $("#btn_fnlz").click(function () { 
        console.log(fecha_hoy)
        console.log(fecha_fini)
        if (totalFinal == 0){
            alert("Añada productos para poder realizar la compra")

        }else if ($("#cuponDes").text() != "Descuento 0.00$ ") {
            if (limite == usado || fecha_hoy >= fecha_fini) {
                alert("Cupon caducado")
                window.location.reload()                   
            }
            else{
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const cod_cupon = $('#inpD').val().trim();
                const usuario = $('#id_user').val();
                calcularTotales()
                const total = totalFinal;

                $.ajax({
                    type: "POST",
                    url: "/updatelimit_cupon/",
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken
                    },
                    data:{
                        'cod_cupon' : cod_cupon,
                        'usuario' : usuario,
                        'total' : total
                    },
                    success: function () {
                        alert("Cupon Valido y Compra Validada Total: " + totalFinal+"$")
                        window.location.href = '/Admin_v/tracking.html/'
                    }
                });
            }
        } else {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const usuario = $('#id_user').val();
            calcularTotales()
            const total = totalFinal;

            $.ajax({
                type: "POST",
                url: "/car_sindes_val/",
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'usuario' : usuario,
                    'total' : total,
                },
                success: function () {
                    alert("Compra Validada Total: " + totalFinal+"$")
                    window.location.href = '/Admin_v/tracking.html/'
                }
            });
        }
    });
});