// Generated by CoffeeScript 1.4.0
var ajax=(function($){
  function started(){
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
    $( "#from" ).datepicker({
      defaultDate: "+1w",
      changeMonth: true,
      numberOfMonths: 3,
      dateFormat: 'yy-mm-dd',
      onClose: function( selectedDate ) {
        $( "#to" ).datepicker( "option", "minDate", selectedDate );
      }
    });
    $( "#to" ).datepicker({
      defaultDate: "+1w",
      changeMonth: true,
      numberOfMonths: 3,
      dateFormat: 'yy-mm-dd',
      onClose: function( selectedDate ) {
        $( "#from" ).datepicker( "option", "maxDate", selectedDate );
      }
    });
  }





  return{
    inicio:started
  }

})(jQuery);

$(document).on('ready', ajax.inicio );