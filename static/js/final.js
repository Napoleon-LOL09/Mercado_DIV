$(document).ready(function () {
    //mapa
    var map = L.map('map').setView([8.4944, -82.5990], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    var currentMarker = null;
    var movingMarker = null;
    var moveInterval = null;
    
    map.locate({ setView: true, maxZoom: 11 });
    
    function onLocationFound(e) {
        var iniciallating = L.latLng($("#latitud").val(), $("#longitud").val());
        var marker = L.marker([$("#latitud").val(), $("#longitud").val()]).addTo(map);
        marker.bindPopup("Posicion Suya<br>" + "Latitud: " + iniciallating.lat.toFixed(4) + "<br>Longitud: " + iniciallating.lng.toFixed(4)).openPopup();
        currentMarker = marker;
    
        var startingLatLng = L.latLng(8.4277, -82.4396); // Coordenadas iniciales del segundo marcador
        movingMarker = L.marker(startingLatLng, { draggable: false }).addTo(map);
        movingMarker.bindPopup("Posicion del Repartidor<br>" + "Latitud: " + startingLatLng.lat.toFixed(4) + "<br>Longitud: " + startingLatLng.lng.toFixed(4)).openPopup();
    
        moveInterval = setInterval(function () {
            moveSecondMarker(iniciallating);
        }, 100); // Actualizar la posición cada 1 segundo
    }
    
    map.on('locationfound', onLocationFound);
    
    function moveSecondMarker(destination) {
        if (movingMarker !== null && destination !== null) {
            var currentLatLng = movingMarker.getLatLng();
            var targetLatLng = destination;
    
            var latDiff = targetLatLng.lat - currentLatLng.lat;
            var lngDiff = targetLatLng.lng - currentLatLng.lng;
    
            var stepLat = latDiff / 100; // Incrementamos la cantidad de pasos
            var stepLng = lngDiff / 100;
    
            var newLat = currentLatLng.lat + stepLat;
            var newLng = currentLatLng.lng + stepLng;
    
            var newLatLng = L.latLng(newLat, newLng);
            movingMarker.setLatLng(newLatLng);
            movingMarker.bindPopup("Posicion Actual Del Repartidor <br>" + "Latitud: " + newLatLng.lat.toFixed(4) + "<br>Longitud: " + newLatLng.lng.toFixed(4)).openPopup();
            
            calcularDistancia(8.4944, -82.5990, newLatLng.lat.toFixed(4), newLatLng.lng.toFixed(4))
            // Verificar si las coordenadas son lo suficientemente cercanas
            var latDiffCheck = Math.abs(targetLatLng.lat - newLatLng.lat);
            var lngDiffCheck = Math.abs(targetLatLng.lng - newLatLng.lng);
    
            if (latDiffCheck <= 0.0005 && lngDiffCheck <= 0.0005) {
                clearInterval(moveInterval);
                setTimeout(function() {
                    const msg = 'Repartidor<br>Ya me encuentro en su casa ';
                    const msgelement = $('<div>').html(msg).addClass('resp_msg mt-2');
                    $(".caja_msg").append(msgelement);
                    $(".caja_msg").scrollTop($(".caja_msg").prop('scrollHeight'));
                  }, 1000);
                $("#gracias, #salir").show()
                $("#distancia, #total").hide()
            }
        }
    }

    let distancia_actual
    function calcularDistancia(lat1, lon1, lat2, lon2) {
        const radioTierra = 6371; // Radio de la Tierra en kilómetros
    
        const dLat = (lat2 - lat1) * (Math.PI / 180);
        const dLon = (lon2 - lon1) * (Math.PI / 180);
    
        const a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * (Math.PI / 180)) * Math.cos(lat2 * (Math.PI / 180)) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
    
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        const distancia = radioTierra * c;
        
        distancia_actual = distancia;
        return distancia; 
    }

    //Chat
    $("#gracias, #salir").hide()

    $("#total").on('click', function() {
        const mensaje = $(this).val();
        mostrar_mensajes(mensaje);
    });

    $("#distancia").on('click', function() {
        const mensaje = $(this).val();
        mostrar_mensajes(mensaje);
    });

    $("#gracias").on('click', function() {
        const mensaje = $(this).val();
        mostrar_mensajes(mensaje);
    });

function mostrar_mensajes(texto) {
    const valor_mensaje = $('<div>').text(texto);
    const nombree = $('#name_user').val()
    $(".caja_msg").append(nombree , valor_mensaje);
    $(".caja_msg").scrollTop($(".caja_msg").prop('scrollHeight'));
    // Mostrar el mensaje de respuesta
    if (texto.toLowerCase().includes('¿cuanto es el total a pagar?')) {
        let total_d = $("#total_d").val()
      setTimeout(function() {
        const msg = 'Repartidor<br>El total a pagar es de ' + total_d+'$';
        const msgelement = $('<div>').html(msg).addClass('resp_msg');
        $(".caja_msg").append(msgelement);
        $(".caja_msg").scrollTop($(".caja_msg").prop('scrollHeight'));
      }, 1000);

    } else if (texto.toLowerCase().includes('¿a cuanto te encuentras?')){
        setTimeout (function (){
        const msg = 'Repartidor<br>Me encuentro a ' + distancia_actual.toFixed(1)+' KM de su ubicación';
        const msgelement = $('<div>').html(msg).addClass('resp_msg');
        $(".caja_msg").append(msgelement);
        $(".caja_msg").scrollTop($(".caja_msg").prop('scrollHeight')); 
        }, 1000) 

    } else if (texto.toLowerCase().includes('gracias')){
        setTimeout (function (){
        const msg = 'Repartidor<br>Gracias a usted por preferirnos';
        const msgelement = $('<div>').html(msg).addClass('resp_msg');
        $(".caja_msg").append(msgelement);
        $(".caja_msg").scrollTop($(".caja_msg").prop('scrollHeight')); 
        }, 1000) 
    }
}

    $("#salir").click(function () { 
            id_delete = $("#total_id").val()
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            $.ajax({
                type: "delete",
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                url: "/delete_total/",
                success: function () {
                    window.location.href = "/Admin_v/menu.html"
                },
                
            });
    });


    $("#hdrctn").hide()

    //Carrito
    $("#carrito_h").hide()
    $("#btncar, #btnLog, #home").click(function () { 
        alert("Compra ya realizada, Espere al repartidor")
    });


});