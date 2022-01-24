from django.db import models
from django.forms import model_to_dict
from AnDjo.settings import MEDIA_URL

# Create your models here.

class ProdServ(models.Model):
    CATEGO_CHOICES = (
        ('P', 'Producto'),
        ('S', 'Servicio'),
    )
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    categoria = models.CharField(max_length=1, choices=CATEGO_CHOICES, default='P')
    thumbnail = models.FileField(verbose_name='Imagen')
    precio = models.FloatField(default=0)
    costo = models.FloatField(default=0, verbose_name='Costo Unitario')
    cantidad_almacen = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] =  self.nombre
        item['categoria'] = self.categoria
        item['thumbnail'] = '{}{}'.format(MEDIA_URL, self.thumbnail)
        item['precio'] =  self.precio
        item['costo'] =  self.costo
        item['cantidad_almacen'] =  self.cantidad_almacen
        return item

    class Meta:
        verbose_name = 'Producto o Servicio'
        verbose_name_plural = 'Productos o Servicios'

class Proveedor(models.Model):
    CATEGO_CHOICES = (
        ('P', 'Productos'),
        ('S', 'Servicios'),
        ('R', 'Recursos'),
    )
    LOCATION_CHOICES = (
        ('N', 'Norte'),
        ('S', 'Sur'),
        ('E', 'Oriente'),
        ('W', 'Poniente'),
    )
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    categoria = models.CharField(max_length=1, choices=CATEGO_CHOICES, verbose_name='Categoria', default='P', unique=False, blank=False)
    tel1 = models.CharField(max_length=15, verbose_name='Teléfono', unique=True, blank=False)
    tel2 = models.CharField(max_length=15, verbose_name='Teléfono 2', unique=False, blank=True)
    mail = models.EmailField(max_length=64, verbose_name='e-mail', unique=False, blank=True)
    address = models.CharField(max_length=264, verbose_name='Dirección', unique=False, blank=True)
    website = models.URLField(max_length=100, verbose_name='Website', unique=False, blank=True)
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES, verbose_name='Ubicación',  default='N')
    keywords = models.CharField(max_length=100, verbose_name='Keywords', unique=False, blank=True)
    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        # item['nombre'] = self.nombre
        # item['categoria'] = self.categoria
        # item['tel1'] = self.tel1
        # item['tel2'] = self.tel2
        # item['mail'] = self.mail
        # item['address'] = self.address
        # item['website'] = self.website
        # item['location'] = self.location
        return item
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']

class Articulo(models.Model):
    CATEGO_CHOICES = (
        ('A', 'Articulo'),
        ('S', 'Servicio'),
    )
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    categoria = models.CharField(max_length=1, choices=CATEGO_CHOICES, default='P')
    precio = models.FloatField(default=0)
    descripcion = models.CharField(max_length=150, verbose_name='Descripción', blank=True, unique=False)
    
    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] =  self.nombre
        item['categoria'] = self.categoria
        item['precio'] =  self.precio
        item['descripcion'] =  self.descripcion
        return item

    class Meta:
        verbose_name = 'Articulo o Servicio'
        verbose_name_plural = 'Articulos o Servicios'