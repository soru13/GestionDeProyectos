
$(document).ready(function() {
    $("#leido").on("click", function(){
      $("#myModal").modal("show");
      $.ajax({
          async:true,
              url: '/InBox/',
              type: 'POST',
              success: function(response) {
                if (response.exito) {
                  $("#leido").html('<img src="/static/base/img/inbox-5-24.ico"/>0 Notificaciones');
                  console.log("exito");
                }
              },
        });
    });

    // agrega clase prettyprint a todos los bloques <pre> (tambien podemos agregar <code>)
    var prettify = false;
    $("pre").each(function() {
        $(this).addClass('prettyprint');
        prettify = true;
    });

    // si se encontro bloques de código se llama la función prettyPrint
    if ( prettify ) {
        $.getScript("/static/base/js/vendor/bootstrap-wysihtml5_files/prettify.js", function() { prettyPrint() });
    }
});