$(document).on 'ready',inicio
inicio=->
	$.ajaxSetup({
		beforeSend: (xhr)->
			xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'))
		})
	$('#formulario').bind 'submit',(e)->
		e.preventDefault()
		fd = new FormData($('#formulario').get(0))
		$.ajax '/',
			url:''
			data:fd
			type:'post'
			success:(data)->
				if data.exito
					$("#resultados").html("<span class='alert alert-success'>Creado Exitosamente</span>")
					$("#formulario").get(0).reset()
				else 
					$("#resultados").html('')
					if data.errores.nombre
						$('<span class="alert alert-error">'+data.errores.nombre+'</span>').appendTo('#resultados')
					if data.errores.apellidos
						$('<span class="alert alert-error">'+data.errores.nombre+'</span>').appendTo('#resultados')
					if data.errores.edad
						$('<span class="alert alert-error">'+data.errores.nombre+'</span>').appendTo('#resultados')
				
			processData:false
			contentType:false