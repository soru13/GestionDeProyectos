// Generated by CoffeeScript 1.4.0
  $(document).on('ready', inicio );
  function inicio(){
     $("#allformulario").show();
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

  };
