$(document).ready(function () {
    var mensaje = $("#reg_ext").text()
    $("#reg_ext").hide()

    if (mensaje.trim() !== ""){
        $("#reg_ext").show()

        setTimeout(function() {
            $("#reg_ext").fadeOut(300, function() {
                window.location.href = "/Admin_v/categorias.html"
            });
        }, 2000);
    }  
    
    $('.edit').on('blur', function() {
        const columna = $(this).data('column');
        const valor = $(this).text().trim();
        const id = $(this).data('id');
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        $.ajax({
            url: '/actualizar_categorias/', 
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            data: {
                'columna': columna,
                'valor': valor,
                'id': id,
            },
            success: function(response) {
                console.log('Datos actualizados correctamente:', response);
            },
            error: function(error) {
                console.error('Error al actualizar los datos:', error);
            }
        });
    });
});
