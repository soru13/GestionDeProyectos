$(document).on 'ready',inicio

inicio=->
	accion = $('#formulario').find('input[type=submit]').val()
	console.log(accion);
	idurl = location.href.substr(location.href.lastIndexOf('/')+1)
	if accion == 'AgregarAct'
		$('#formulario').bind 'submit',(e)->
		e.preventDefault()
		url = '/NuevaActividadAjax/'
		fd = new FormData($('#formulario').get(0))
		$('#exito').attr({'title':'Proyectos','href':'/ControlActividades'})
		$.ajax '/',
            url: url,
            data: fd,
            type: 'POST',
            success: (data)->
            	if data.exito
                	$("#resultados").html("<span class='alert alert-success'>Creado Exitosamente</span>")
                if accion == 'AgregarAct'
                  $("#formulario").get(0).reset()
                  $("#exito").show()
                if accion == 'TerminarAct'
                  $("#exito").show()
             	else 
                	$("#resultados").html('')
                if data.errores.Actividad 
                	$('<span class="alert alert-error"><b>Actividad </b>' + data.errores.Actividad + '</span>').appendTo('#resultados')
                
                if data.errores.Hasta
                	$('<span class="alert alert-error"><b>Hasta </b>' + data.errores.Hasta + '</span>').appendTo('#resultados')
                
                if data.errores.Desde 
                 	$('<span class="alert alert-error"><b>Desde </b>' + data.errores.Desde + '</span>').appendTo('#resultados')
                
                if data.errores.proyecto
                  	$('<span class="alert alert-error"><b>proyecto </b>' + data.errores.proyecto + '</span>').appendTo('#resultados')
            processData: false,
            contentType: false
    if accion == 'Agregar'
		$('#formulario').bind 'submit',(e)->
		e.preventDefault()
		url = '/AgregarProyectoAjax/'
		fd = new FormData($('#formulario').get(0))
		$('#exito').attr({'title':'Proyectos','href':'/ControlActividades'})
		$.ajax '/',
            url: url,
            data: fd,
            type: 'POST',
            success: (data)->
            	if data.exito
                	$("#resultados").html("<span class='alert alert-success'>Creado Exitosamente</span>")
                if accion == 'Agregar'
                  $("#formulario").get(0).reset()
                  $("#exito").show()
                if accion == 'Terminar'
                  $("#exito").show()
             	else 
                	$("#resultados").html('')
                if data.errores.Proyecto 
                	$('<span class="alert alert-error"><b>Proyecto </b>' + data.errores.Proyecto + '</span>').appendTo('#resultados')
                
                if data.errores.Usuario
                	$('<span class="alert alert-error"><b>Usuario </b>' + data.errores.Usuario + '</span>').appendTo('#resultados')
            processData: false,
            contentType: false
