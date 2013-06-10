define([
		'modulos/contador'
	],function(){
	return{
		Iniciar: function(){
			for(var name in modulos){
				modulos[name].Iniciar();
			}
		}
	}
});