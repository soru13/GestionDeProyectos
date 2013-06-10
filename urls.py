from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()


from tastypie.api import Api
from API.api.resources import UserResource, LineaResource, MonedasResource, FormasPagoResource, UnidadesMedidaResource, BancosResource, EmpresasResource, ProductosResource, ClientesResource, CuentasClientesResource, FacturasResource

v1_api = Api()
v1_api.register(UserResource())
v1_api.register(LineaResource())
v1_api.register(MonedasResource())
v1_api.register(FormasPagoResource())
v1_api.register(UnidadesMedidaResource())
v1_api.register(BancosResource())
v1_api.register(EmpresasResource())
v1_api.register(ProductosResource())
v1_api.register(ClientesResource())
v1_api.register(CuentasClientesResource())
v1_api.register(FacturasResource())

urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
    # Examples:
    url(r'^CFDI$', 'API.views.CFDI', name='CFDI'),
    url(r'^Developers$', 'API.views.desarrolladores', name='desarrolladores'),
    

    url(r'^Usuarios$', 'Usuarios.views.usuarios', name='usuarios'),
    url(r'^NuevoUsuario$', 'Usuarios.views.NuevoUsuario', name='NuevoUsuario'),
    url(r'^NuevoUsuarioAjax/$', 'Usuarios.views.AgregarUsuarioAjax', name='NuevoUsuario'),
    url(r'^EditarPerfilLogin/$', 'Usuarios.views.EditarPerfilLogin', name='EditarPerfilLogin'),
    url(r'^EditarUsuario/(?P<id_usuario>\d+)$', 'Usuarios.views.EditarPerfil', name='editar'),
    url(r'^EditarUsuarioAjax/$', 'Usuarios.views.EditarUsuarioAjax', name='EditarUsuarioAjax'),
    url(r'^borrarUsuario/(?P<id_usuario>\d+)$', 'Usuarios.views.eliminar', name='eliminar'),
    url(r'^resetPassword$', 'Usuarios.views.resetPassword', name='resetPassword'),
    url(r'^ingresar$','Usuarios.views.ingresar'),
    url(r'^cerrar$', 'Usuarios.views.cerrar'),
    

    url(r'^$', 'Home.views.Principal'),
    url(r'^addActividades/(?P<id_Actividad>\d+)$', 'Home.views.addActividades'),
    url(r'^estadisticas$', 'statistics.views.statistics'),
    url(r'^search/$', 'Home.views.search'),
    url(r'^InBox/$', 'Home.views.InBox', name='InBox'),
    url(r'^leidos/$', 'Chat.views.leidos', name='leidos'),
    url(r'^Correo/$', 'Chat.views.Correo', name='Correo'),
    url(r'^NuevaNotificacion/(?P<id_Actividad>\d+)$', 'Chat.views.NuevaNotificacion', name='NuevaNotificacion'),
    url(r'^ResponderNotificacion/(?P<id_Actividad>\d+)/(?P<id_Usuario>\d+)$', 'Chat.views.ResponderNotificacion', name='ResponderNotificacion'),
    url(r'^Chat$', 'Chat.views.Chat', name='Chat'),
    url(r'^Mensaje/(?P<id_Usuario>\d+)$', 'Chat.views.Mensaje', name='Mensaje'),
    url(r'^MensajeAjax/$', 'Chat.views.MensajeAjax', name='MensajeAjax'),



    #url(r'^$', 'Apps.views.Apps', name='Apps'),
    url(r'^Apps$', 'Apps.views.Appsprivada', name='Apps'),
    url(r'^AgregarAplicacion$', 'Apps.views.AgregarAplicacion', name='Apps'),
    url(r'^filter/$', 'ControlActividades.views.filter'),
    url(r'^ControlActividades$', 'ControlActividades.views.ControlActividades', name='ControlActividades'),
    url(r'^AgregarProyecto$', 'ControlActividades.views.AgregarProyecto', name='AgregarProyecto'),
    url(r'^AgregarProyectoAjax/$', 'ControlActividades.views.AgregarProyectoAjax', name='AgregarProyectoAjax'),
    url(r'^GetDataProyectoJson/(?P<id_proyecto>\d+)$', 'ControlActividades.views.GetDataProyectoJson', name='Editar'),
    #url(r'^GetDataProyectoJsonLast$', 'ControlActividades.views.GetDataProyectoJsonLast', name='GetDataProyectoJsonLast'),
    url(r'^EditarProyectoAjax/(?P<id_proyecto>\d+)$', 'ControlActividades.views.EditarProyectoAjax', name='EditarAjax'),
    url(r'^eliminarAjax/(?P<id_proyecto>\d+)$', 'ControlActividades.views.eliminarAjax', name='eliminarAjax'),

    url(r'^Actividades/(?P<id_proyecto>\d+)$', 'ControlActividades.views.Actividades', name='Avtividades'),
    url(r'^NuevaActividad/(?P<id_proyecto>\d+)$', 'ControlActividades.views.NuevaActividad', name='NuevaActividad'),
    url(r'^NuevaActividadAjax/$', 'ControlActividades.views.NuevaActividadAjax', name='AddAvtividadAjax'),

    url(r'^GetDataActividadJson/(?P<id_Actividad>\d+)$', 'ControlActividades.views.GetDataActividadJson', name='GetDataActividadJson'),
    url(r'^EditarAct/(?P<id_Actividad>\d+)/(?P<id_proyecto>\d+)$', 'ControlActividades.views.EditarAct', name='EditarAct'),
    url(r'^EditarActAjax/(?P<id_Actividad>\d+)$', 'ControlActividades.views.EditarActAjax', name='EditarActAjax'),

    url(r'^finalizarActAjax/(?P<id_Actividad>\d+)$', 'ControlActividades.views.finalizarActAjax', name='finalizarActAjax'),
    url(r'^EliminarActAjax/(?P<id_Actividad>\d+)$', 'ControlActividades.views.EliminarActAjax', name='EliminarActAjax'),

    url(r'^Avances/(?P<id_Actividad>\d+)/(?P<id_proyecto>\d+)$', 'ControlActividades.views.Historial', name='Historial'),
    url(r'^GetDataAvanceJsonLast/$', 'ControlActividades.views.GetDataAvanceJsonLast', name='GetDataAvanceJsonLast'),
    url(r'^AgregarAvanceAjax/$', 'ControlActividades.views.AgregarAvanceAjax', name='AddAAgregarAvance'),
    
    url(r'^Reporteria$', 'Reporteria.views.Reporteria', name='Reporteria'),

    #url(r'^add/$', 'Apps.views.Agregar_Usuario', name='Agregar_Usuario'),
    #url(r'^borrar/(?P<id_usuario>\d+)$', 'Apps.views.eliminar', name='eliminar'),
    #url(r'^editar/(?P<id_usuario>\d+)$', 'Apps.views.editar', name='editar'),
    #url(r'^Aeditar_perfil/$', 'Apps.views.editar_perfil', name='Aeditar_perfil'),
    # url(r'^HCC/', include('HCC.foo.urls')),
    url(r'^live$', 'streaming.views.live', name='live'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)#expresiones regulares
urlpatterns += staticfiles_urlpatterns()