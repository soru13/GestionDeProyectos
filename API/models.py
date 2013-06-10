from django.db import models
from django.contrib.auth.models import User

from tastypie.utils.timezone import now
from django.template.defaultfilters import slugify

from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)

class Lineas(models.Model):
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField(auto_now=True)
    Descripcion = models.CharField(max_length=200,unique=True)
    Estatus = models.BooleanField(default=True)
    def __unicode__(self):
        return self.Descripcion
        
class Monedas(models.Model):
	Descripcion = models.CharField(max_length=100)
	ValorPeso = models.DecimalField(max_digits=10,decimal_places=2)
	Estatus = models.BooleanField(default=True)
	Fecha= models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.Descripcion

class FormasPago(models.Model):
	Descripcion = models.CharField(max_length=100)
	Estatus = models.BooleanField(default=True)
	user = models.ForeignKey(User)
	Fecha= models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.Descripcion

class UnidadesMedida(models.Model):
	Descripcion = models.CharField(max_length=100,unique=True)
	Estatus = models.BooleanField(default=True)
	Fecha= models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.Descripcion

class Bancos(models.Model):
	Descripcion = models.CharField(max_length=100)
	Direccion = models.TextField()
	Ciudad = models.CharField(max_length=50)

	PersonaContacto = models.CharField(max_length=200)
	PuestoContacto = models.CharField(max_length=100)
	TelefonoContacto = models.CharField(max_length=20)
	FaxContacto = models.CharField(max_length=20)
	EmailContacto = models.EmailField(max_length=150)
	Estatus = models.BooleanField(default=True)
	Fecha= models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User)


	def __unicode__(self):
		return self.Descripcion
		
# Create your models here.
class Empresas(models.Model):
	RFC = models.CharField(max_length=15,unique=True)
	RazonSocial = models.CharField(max_length=200)
	NombreComercial = models.CharField(max_length=200)
	Calle = models.CharField(max_length=50)
	NumeroExt = models.CharField(max_length=10)
	NumeroInt = models.CharField(max_length=10)
	CodigoPostal = models.CharField(max_length=10)

	Colonia = models.CharField(max_length=50)
	Localidad = models.CharField(max_length=50)
	Municipio = models.CharField(max_length=50)
	Estado = models.CharField(max_length=50)
	Pais = models.CharField(max_length=50)
	CalleExp = models.CharField(max_length=50)

	NumeroExteriorExp = models.CharField(max_length=10)
	NumeroInteriorExp = models.CharField(max_length=10)
	CodigoPostalExp = models.CharField(max_length=10)

	ColoniaExp = models.CharField(max_length=50)
	LocalidadExp = models.CharField(max_length=50)
	MunicipioExp = models.CharField(max_length=50)
	EstadoExp = models.CharField(max_length=50)
	PaisExp = models.CharField(max_length=50)

	Telefono = models.CharField(max_length=20)
	Curp = models.CharField(max_length=30,unique=True)
	Fax = models.CharField(max_length=20)

	CorreoElectronico = models.EmailField(max_length=150)
	PaginaWeb = models.URLField(max_length=150)
	Fax = models.CharField(max_length=20)
	Fecha= models.DateTimeField(auto_now=True)
	Estatus = models.BooleanField(default=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.NombreComercial

class Productos(models.Model):
	Codigo = models.CharField(max_length=50)
	CodigoAlterno = models.CharField(max_length=50)
	Descripcion = models.CharField(max_length=100)
	DescripcionLarga = models.CharField(max_length=300)
	StockMinimo = models.DecimalField(max_digits=10,decimal_places=2)
	StockMaximo = models.DecimalField(max_digits=10,decimal_places=2)
	TasaIva = models.DecimalField(max_digits=10,decimal_places=2)
	Precio = models.DecimalField(max_digits=10,decimal_places=2)
	Estatus = models.BooleanField(default=True)
	Fecha= models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User)
	medida = models.ForeignKey(UnidadesMedida)
	#Avatar = models.ImageField(upload_to='AvatarProducto')
	def __unicode__(self):
		return self.Descripcion




class Clientes(models.Model):
	RFC = models.CharField(max_length=20,unique=True)
	RazonSocial = models.CharField(max_length=250)
	Calle = models.CharField(max_length=50)
	NumeroExt = models.CharField(max_length=10)
	NumeroInt = models.CharField(max_length=10)
	Colonia = models.CharField(max_length=50)
	CodigoPostal = models.CharField(max_length=10)
	Localidad = models.CharField(max_length=50)
	Ciudad = models.CharField(max_length=50)
	Estado = models.CharField(max_length=50)
	Pais = models.CharField(max_length=50)
	TieneCredito = models.BooleanField(default=True)
	LimiteCredito = models.DecimalField(max_digits=10,decimal_places=2)
	PlazoDiasCredito = models.IntegerField()
	Telefono = models.CharField(max_length=18)
	TelefonoFax = models.CharField(max_length=180)
	Telefono2 = models.CharField(max_length=180)
	Telefono3 = models.CharField(max_length=180)
	CorreoElectronico = models.EmailField(max_length=150)
	PaginaWeb = models.URLField(max_length=150)
	user = models.ForeignKey(User)
	Fecha= models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.RazonSocial

class CuentasClientes(models.Model):
	Cuenta = models.ForeignKey(Clientes)
	NumeroCuenta = models.CharField(max_length=20)
	user = models.ForeignKey(User)
	Empresa = models.ForeignKey(Empresas)
	Bancos = models.ForeignKey(Bancos)
	Estatus = models.BooleanField(default=True)
	Fecha= models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.NumeroCuenta

class MedidasProductos(models.Model):
	CodigoProducto = models.CharField(max_length=50)
	Medida = models.IntegerField()
	Estatus = models.BooleanField(default=True)

	Equivalencia = models.IntegerField()
	Precio = models.DecimalField(max_digits=10,decimal_places=2)
	Costo = models.DecimalField(max_digits=10,decimal_places=2)
	Fecha= models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.CodigoProducto	

class Facturas(models.Model):
	Empresa = models.ForeignKey(Empresas)
	CuentaPago = models.ForeignKey(CuentasClientes)
	FormaPago = models.ForeignKey(FormasPago)
	Moneda = models.ForeignKey(Monedas)
	Cliente = models.ForeignKey(Clientes)
	user = models.ForeignKey(User)
	FechaCancelacion = models.CharField(max_length=15,default="")
	FechaReimpresion = models.CharField(max_length=15,default="")
	CondicionPago = models.CharField(max_length=1)
	RfcCliente = models.CharField(max_length=20)
	Estatus = models.BooleanField(default=True)
	FechaEmision = models.DateTimeField(auto_now=True)
	

	

class DetalleFacturas(models.Model):
	FolioFactura = models.IntegerField()
	Empresa = models.ForeignKey(Empresas)
	CodigoProducto = models.CharField(max_length=50)
	Cantidad = models.IntegerField()
	Precio = models.DecimalField(max_digits=10,decimal_places=2)
	Importe = models.DecimalField(max_digits=10,decimal_places=2)
	PorcientoDescto = models.IntegerField()
	Descuento = models.DecimalField(max_digits=10,decimal_places=2)
	TasaIva = models.IntegerField()
	Iva = models.DecimalField(max_digits=10,decimal_places=2)
	FechaEmision = models.DateTimeField()
	FechaCancelacion = models.DateTimeField()
	FechaReimpresion = models.DateTimeField()
	CondicionPago = models.CharField(max_length=2)
	Estatus = models.BooleanField(default=True)
	CuentaPago = models.ForeignKey(CuentasClientes)
	Moneda = models.ForeignKey(Monedas)
	FormaPago = models.ForeignKey(FormasPago)
	Cliente = models.ForeignKey(User)
	Fecha= models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.FolioFactura