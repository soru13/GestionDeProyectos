import datetime
from django.contrib.auth.models import User
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer
from tastypie import fields
from API.models import *
try:
    import lxml
    from lxml.etree import parse as parse_xml
    from lxml.etree import Element, tostring
except ImportError:
    lxml = None
try:
    import yaml
    from django.core.serializers import pyyaml
except ImportError:
    yaml = None


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']#lo que no quiero mostrar
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])
        #allowed_methods = ['get']#Solo peticiones GET
        filtering = {
            'username': ALL,
        }
        #excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = DjangoAuthorization()

class LineaResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Lineas.objects.all()
        resource_name = 'Lineas'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }

class MonedasResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Monedas.objects.all()
        resource_name = 'Monedas'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }

class FormasPagoResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = FormasPago.objects.all()
        resource_name = 'FormasPago'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }

class UnidadesMedidaResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = UnidadesMedida.objects.all()
        resource_name = 'UnidadesMedida'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
        

class BancosResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Bancos.objects.all()
        resource_name = 'Bancos'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }


class EmpresasResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Empresas.objects.all()
        resource_name = 'Empresas'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }

class ProductosResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    medida = fields.ForeignKey(UnidadesMedidaResource, 'medida')
    class Meta:
        queryset = Productos.objects.all()
        resource_name = 'Productos'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }

class ClientesResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Clientes.objects.all()
        resource_name = 'Clientes'
        authorization = Authorization()
        filtering = {
            "slug": ('exact', 'startswith',),
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }

class CuentasClientesResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    Cuenta = fields.ForeignKey(ClientesResource, 'Cuenta')
    Empresa = fields.ForeignKey(EmpresasResource, 'Empresa')
    Bancos = fields.ForeignKey(BancosResource, 'Bancos')
    class Meta:
        queryset = CuentasClientes.objects.all()
        resource_name = 'CuentasClientes'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }

        
class FacturasResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    Empresa = fields.ForeignKey(EmpresasResource, 'Empresa')
    CuentaPago = fields.ForeignKey(CuentasClientesResource, 'CuentaPago')
    FormaPago = fields.ForeignKey(FormasPagoResource, 'FormaPago')
    Moneda = fields.ForeignKey(MonedasResource, 'Moneda')
    Cliente = fields.ForeignKey(ClientesResource, 'Cliente')
    class Meta:
        queryset = Facturas.objects.all()
        resource_name = 'Facturas'
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = DjangoAuthorization()
