# Create your views here.
# views.py - sample view

from soaplib_handler import DjangoSoapApp, soapmethod, soap_types


class HelloWorldService(DjangoSoapApp):

    __tns__ = 'http://my.namespace.org/soap/'

    @soapmethod(soap_types.String, soap_types.Integer, _returns=soap_types.Array(soap_types.String))
    def say_hello(self, name, times):
        results = []
        for i in range(0, times):
            results.append('Hello, %s'%name)
        return results

hello_world_service = HelloWorldService()