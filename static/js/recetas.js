$(document).ready(function () {
    function Autoselect () {  
        $("#lblV").show()
        $("#lblV").after('<br id=brV>')
        $("#frmVideo").after('<br id=brFV>')
        $("#slcTR").after('<br id=brTR>')

        $("#tipo").val("Video")
    }
    Autoselect()

    function manualSelect (){
        $("#slcTR").change(function (e) { 
            e.preventDefault();
            var opcion = $("#slcTR").val();    
            $('#frmIngre, #frmProce, #frmVideo, #lblV, #lblP, #lblI').hide()
            $('#brFV, #brV, #brTR, #br1, #br2, #br3, #br4, #br5').remove()
            

            if (opcion == "Video") {
                $("#frmVideo, #lblV").show()
                $("#lblV").after('<br id=brV>')
                $("#frmVideo").after('<br id=brFV>')
                $("#slcTR").after('<br id=brTR>')

                $("#tipo").val(opcion)
    
            } else if (opcion == "Escrito") {
                $("#frmIngre, #frmProce, #lblP, #lblI").show()
                $("#slcTR").after ('<br id="br1">');
                $("#frmIngre").after ('<br id="br2">');
                $("#frmProce").after ('<br id="br3">');
                $("#lblI").after ('<br id="br4">')
                $("#lblP").after('<br id="br5">')

                $("#tipo").val(opcion)
            }
        });
    }
    manualSelect()

    var tablaoriginal = $('#tblR tbody').html();
    var paginador = $('#thPAG').html();
    
    $('.cat').click(function (e) {
        e.preventDefault();
        var categoria = $(this).data('categoria');
        
        if (categoria == "todos"){
            $('#tblR tbody').html(tablaoriginal)
            $('#thPAG').html(paginador)

        }else{
            $.ajax({
                type: 'GET',
                url: '/filtrar_recetas/', 
                data: {
                    categoria: categoria
                },
                success: function (data) {
                    $('#tblR tbody').empty();
                    $('#thPAG').empty();
                    var recetas = data.recetas;
                    var rows = Math.ceil(recetas.length / 2); 
                    
                    for (var i = 0; i < rows; i++) {
                        var newRow = '<tr>';
                        for (var j = 0; j < 2; j++) {
                            var index = i * 2 + j;
                            if (index < recetas.length) {
                                // Construir la fila de la tabla con los datos de la receta
                                newRow += '<td>' +
                                    '<div class="imgCtn">' +
                                    '<a href="/Admin_v/ver_receta.html/' + recetas[index].id +  ' "><img src="' + recetas[index].imagen + '" alt=""></a>' +
                                    '<div class="nombre">' + recetas[index].nombre + '</div>' +
                                    '<div class="catego">' + recetas[index].categoria + '</div>' +
                                    '</div>' +
                                    '</td>';
                            } else if (index === recetas.length && recetas.length % 2 !== 0) {
                                // Agregar una columna en blanco si hay un número impar de recetas
                                newRow += '<td style="width: 100%; padding-left: 381px; box-sizing: border-box;  visibility: hidden;">  </td>';
                            }
                        }
                        newRow += '</tr>';
                        $('#tblR tbody').append(newRow); // Agregar la nueva fila a la tabla
                    }
                },
                error: function (error) {
                    console.log('Error en la solicitud AJAX: ', error);
                }
            });
        }
    });

    $('#search_R').on('input', function() {
        var resultados = $(this).val();
    
        $.ajax({
            type: 'GET',
            url: '/User_v/recetas.html',
            data: {
                'search_R': resultados
            },
            success: function(response) {
                var recetas_filtradas = response.filtrado;
                if (resultados != "") {
                    $('#result_fil').show();
                    mostrarResultados(recetas_filtradas)
                } else
                    $('#result_fil').hide();
            }
        });
    });

    function mostrarResultados(respuesta) {
        var html = '';
        for (var i = 0; i < respuesta.length; i++) {
            html += '<div>';
            html += '<a style="font-size: 19px" href="/User_v/ver_receta.html/' + respuesta[i].id + '">' + respuesta[i].nombre + '</a>';
        }

        $('#result_fil').html(html);
        $('#result_fil a').on('click', function(event) {
            event.preventDefault();
            var href = $(this).attr('href');
            window.location.href = href;
        });
    }
    

    $('input[type="radio"]').click(function() {
        var opcion = $(this).val();

        if (opcion === 'existente') {
            $('#divexist').show();
            $('#divnueva').hide();
        } else if (opcion === 'nueva') {
            $('#divnueva').show();
            $('#divexist').hide();
        }
    });

});


