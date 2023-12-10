$(document).ready(function () {
//Mapa Javascript
    var map = L.map('map').setView([8.4944, -82.5990], 90);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
    }).addTo(map);

    var radius = 10;
    var currentMarker = null;
    var radios = null;

    map.locate({ setView: true, maxZoom: 16 });

        function onLocationFound(e) {
            var marker = L.marker(e.latlng).addTo(map);
            marker.bindPopup("Posicion Actual<br>" + "Latitud: " + e.latlng.lat.toFixed(4) + "<br>Longitud: " + e.latlng.lng.toFixed(4)).openPopup();
            radio = L.circle(e.latlng, radius).addTo(map);
            currentMarker = marker
            radios = radio
            $("#latitud").val(e.latlng.lat.toFixed(4))
            $("#longitud").val(e.latlng.lng.toFixed(4))
        }

        map.on('locationfound', onLocationFound); 

        map.on('click', function(e) {
            if (currentMarker !== null) {
                map.removeLayer(currentMarker);
                map.removeLayer (radios)
            }

            var newMarker = L.marker(e.latlng).addTo(map);
            newMarker.bindPopup("Nueva Posición<br>Latitud: " + e.latlng.lat.toFixed(4) + "<br>Longitud: " + e.latlng.lng.toFixed(4)).openPopup();
            radio = L.circle(e.latlng, radius).addTo(map);
            currentMarker = newMarker;
            radios = radio
            $("#latitud").val(e.latlng.lat.toFixed(4))
            $("#longitud").val(e.latlng.lng.toFixed(4))
        });

        
    //Demas Codigo
    //Validadores de Campos
    $('#ma').on('input', function(e) {
        let input = $(this).val().replace(/\D/g, '').substring(0, 4);
        let mes = input.substring(0, 2);
        let año = input.substring(2, 4);
    
        if (input.length > 2) {
          $(this).val(mes + '/' + año);
        } else {
          $(this).val(input);
        }
      });

    $('#nt').on('input', function(e) {
        let input = $(this).val().replace(/[^\d]/g, '').substring(0, 16);
        let restringir = input.replace(/(\d{4})(?=\d)/g, '$1 ');

        $(this).val(restringir);
    });  

    $('#cds').on('input', function(e) {
        let input = $(this).val().replace(/\D/g, '').substring(0, 3);
    
        if (input.length > 2) {
          $(this).val(input);
        }
    });  

    $('#id_cel').on('input', function(e) {
        let input = $(this).val().substring(0, 8);
        $(this).val(input);
    });

    $('#id_cedula').on('input', function() {
        var input = $(this).val();
        var prohibir = /^[0-9-]+$/;
    
        if (!prohibir.test(input)) {
          $(this).val(input.slice(0, -1));
        }
    });

    function sololetras (campo) {
        $(campo).on('input', function(e) {
            let prohibido = $(this).val().replace(/[^A-Za-zÁÉÍÓÚáéíóúñÑ\s]/g, '');
        
            $(this).val(prohibido);
        })
    }
    
    sololetras($("#name"))
    sololetras($("#id_ciudad"))
    sololetras($("#id_provincia"))



    //Finalizacion de los datos
    $("#tarjetaa").hide()
    var pagoo = null
    
    function ocultar_mostrar (label, input) {  
        $(input).on('input', function(){
                if ($(this).val() != 0){
                    $(label).show()
                } else {
                    $(label).hide()
                }
            })
    }

    $('input[type="radio"]').click(function () { 
        var opcion = $(this).val()

        if (opcion == 'tarjeta') {
            $("#tarjetaa").show();
            $('#lnt, #lma, #lcds').hide()

            ocultar_mostrar($("#lnt"), $("#nt"))
            ocultar_mostrar($("#lma"), $("#ma"))
            ocultar_mostrar($("#lcds"), $("#cds"))
            ocultar_mostrar($("#lname"), $("#name"))

            pagoo = opcion  
        } else {
            $("#tarjetaa").hide();
            pagoo = opcion
        }
    });

    /* Selector */
    $("#btn_ce").hide()
    $("#slct_exist").hide()

    function funciones_oculte () {
        $("#btn_ce").hide();
        $("#slct_exist").hide();
        $("#btn_c").show();

        $("#tarjetaa").hide()
        $("#id_cel").val("").prop('readonly', false);
        $("#id_cedula").val("").prop('readonly', false);
        $("#id_provincia").val("").prop('readonly', false);
        $("#id_ciudad").val("").prop('readonly', false);
        $("#id_barrio").val("").prop('readonly', false);
        $('input[name="pago"]').prop('disabled', false);
        $("#tarjeta").prop('checked', false);
        $("#nt, #name, #cds, #ma").val("").prop('readonly', false);
        $("#efectivo").prop('checked', false);

         // Eliminar el mapa existente
         if (map !== null) {
            map.remove();
        }

        // Volver a crear el mapa
        map = L.map('map').setView([8.4944, -82.5990], 90);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
        }).addTo(map);

        var radius = 10;
        var currentMarker = null;
        var radios = null;

        map.locate({ setView: true, maxZoom: 16 });

            function onLocationFound(e) {
                var marker = L.marker(e.latlng).addTo(map);
                marker.bindPopup("Posicion Actual<br>" + "Latitud: " + e.latlng.lat.toFixed(4) + "<br>Longitud: " + e.latlng.lng.toFixed(4)).openPopup();
                radio = L.circle(e.latlng, radius).addTo(map);
                currentMarker = marker
                radios = radio
                $("#latitud").val(e.latlng.lat.toFixed(4))
                $("#longitud").val(e.latlng.lng.toFixed(4))
            }

            map.on('locationfound', onLocationFound); 

            map.on('click', function(e) {
                if (currentMarker !== null) {
                    map.removeLayer(currentMarker);
                    map.removeLayer (radios)
                }
    
                var newMarker = L.marker(e.latlng).addTo(map);
                newMarker.bindPopup("Nueva Posición<br>Latitud: " + e.latlng.lat.toFixed(4) + "<br>Longitud: " + e.latlng.lng.toFixed(4)).openPopup();
                radio = L.circle(e.latlng, radius).addTo(map);
                currentMarker = newMarker;
                radios = radio
                $("#latitud").val(e.latlng.lat.toFixed(4))
                $("#longitud").val(e.latlng.lng.toFixed(4))
            });
    }

    $("#slct_opc").change(function () {
    if ($("#slct_opc").val() === 'new' || $(this).prop('selectedIndex') === 0) {
        funciones_oculte();

    } else {
        $("#btn_ce").show();
        $("#slct_exist").show();
        $("#btn_c").hide();

        $.ajax({
            type: "GET",
            url: '/obtener_envios/',
            success: function (data) {
                $("#slct_exist").empty();
                if (data.length === 0 || !Array.isArray(data)) {
                    alert("No tienes formularios registrados");
                    $("#slct_opc").prop('selectedIndex', 0);
                    funciones_oculte(); 
                } else {
                    $("#slct_exist").append('<option value="">' + 'Seleccione un formulario' + '</option>');
                    for (let i = 0; i < data.length; i++) {
                        $("#slct_exist").append('<option value="' + data[i].save + '">' + data[i].save + '</option>');
                    }
                }
            }
        });
    }
    });

    $("#slct_exist").change(function () { 
        slecci = $(this).val()

        $("#id_cel").prop('readonly', true)
        $("#id_cedula").prop('readonly', true)
        $("#id_provincia").prop('readonly', true)
        $("#id_ciudad").prop('readonly', true)
        $("#id_barrio").prop('readonly', true)
        
        $.ajax({
            type: "GET",
            url: "/obtener_envios/",
            data: {
                'slecci' : slecci
            },
            success: function (data) {
                for (let i = 0; i < data.length; i++ ){
                    $("#id_cel").val(data[i].cel)
                    $("#id_cedula").val(data[i].cedula)
                    $("#id_provincia").val(data[i].prov)
                    $("#id_ciudad").val(data[i].ciudad)
                    $("#id_barrio").val(data[i].barrio)
                    $("#latitud").val(data[i].lati)
                    $("#longitud").val(data[i].longi)
                    $("#id").val(data[i].id)

                    if (currentMarker !== null) {
                        map.remove()
                    }
                    
                    // Crear un nuevo mapa y un nuevo marcador con la nueva ubicación
                    var newMap = L.map('map').setView([data[i].lati, data[i].longi], 90);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
                    }).addTo(newMap);
    
                    var radius = 10;
                    var newLatLng = L.latLng(data[i].lati, data[i].longi);
                    var newMarker = L.marker(newLatLng).addTo(newMap);
                    newMarker.bindPopup("Posición Actual <br>Latitud: " + data[i].lati + "<br>Longitud: " + data[i].longi).openPopup();
                    var newRadio = L.circle(newLatLng, radius).addTo(newMap);
    
                    // Actualizar las variables globales con el nuevo mapa y el nuevo marcador
                    map = newMap;
                    currentMarker = newMarker;
                    radios = newRadio;


                    if (data[i].pago == 'tarjeta'){
                        $("#tarjeta").prop('checked', true)
                        $("#tarjetaa").show()
                        $('input[name="pago"]').prop('disabled', true)
                        $("#nt").val(data[i].tarjeta).prop('readonly', true)
                        $("#name").val(data[i].titular).prop('readonly', true)
                        $("#cds").val(data[i].segu).prop('readonly', true)
                        $("#ma").val(data[i].mesaño).prop('readonly', true)
                    } else {
                        $("#efectivo").prop('checked', true)
                        $('input[name="pago"]').prop('disabled', true)
                        $("#nt").val("")
                        $("#name").val("")
                        $("#cds").val("")
                        $("#ma").val("")
                        $("#tarjetaa").hide()
                    }
                }
                
            }
        });
    });
    
    /* Modal del Envio */
    $('#confirmSave').click(function(){
        $('#confirmModal #formNameInput').show();
        $('#confirmSave, #btn_no').hide(); 
        $('#saveForm, #dontSave').show(); 
    });

    $('#dontSave').click(function (e) { 
        $('#confirmModal #formNameInput').hide()
        $('#confirmSave, #btn_no').show(); 
        $('#saveForm, #dontSave').hide(); 
    });

    $("#btn_no").click(function (e) { 
        $("#opcion").val('No')
    });

    $("#saveForm").click(function (e) { 
        $("#opcion").val('Si')
    });

    /*Mensaje de Error*/
    
    if ($("#error").val() !== undefined) {
        errorr = $("#error").val()
        alert(errorr)
    }
});