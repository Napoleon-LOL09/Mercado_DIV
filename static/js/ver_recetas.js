$(document).ready(function () {
    tipo = $("#tipo").data('tipo');

    if (tipo == "Escrita") {
        $("#Divideo").remove();
        $("#tblImg").show()
    } else {
        $("#tblImg").remove();
        $("#Divideo").show()
    }
    
});

