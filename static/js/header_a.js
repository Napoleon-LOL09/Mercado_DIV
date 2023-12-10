$(document).ready(function () {
    $("#hdrctn").hide()

    $("#secciones").click(function () { 
        $("#hdrctn").slideToggle();
    });

    $("#btnLog").click(function () { 
        window.location.href = "/../logout"
    });

    $("#home").click(function () { 
        window.location.href = "/Admin_v/menu.html"
    });

    //Carrito
    $("#carrito_h").hide()
    $("#btncar").click(function () { 
        $("#carrito_h").slideToggle()
    });

    function subtotal() {
        var SubtotalF = 0;
            $('.producto').each(function() {
                var precio = $(this).data('precio');
                var cantidad = $(this).data('cantidad');
                var subtotal = precio * cantidad;
                SubtotalF += subtotal;
            });
        
        $("#subtotall").text('Subtotal: $' + SubtotalF)
    }
    subtotal()        

    
    $(".producto").each(function() {
        var pro_id = $(this).data('proo');
        if (pro_id == 30 || pro_id == 31) {        
            $(".producto[data-proo='30'], .producto[data-proo='31']").find(".increment, .decrement").hide();
        }

    });    

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
            
            $.ajax({
                url: '/actualizar_cantidad/' + productoId + '/',
                type: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                data: { 'cantidad': cantidad },
                success: function() {
                    subtotal();
                }
             });
        }else if(action === 'decrement') {
            if (cantidad > 1) {
                cantidad--;
                row.data('cantidad', cantidad);
                row.find('.cantidad').text(cantidad);
                
                $.ajax({
                    url: '/actualizar_cantidad/' + productoId + '/',
                    type: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken
                    },
                    data: 
                    {'cantidad': cantidad },
                    success: function() {
                        subtotal();
                    }
                });
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
                        subtotal()

                        if ($('.producto').length === 0) {
                            window.location.reload()
                        }
                    }
                });
                
            }
        }
    });
});