from django.db import models
from django.forms import model_to_dict
from AnDjo.settings import STATIC_URL, MEDIA_URL

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

# class Servicio(models.Model):
#     nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
#     thumbnail = models.FileField(verbose_name='Imagen')
#     precio = models.FloatField(default=0)
#     costo = models.FloatField(default=0, verbose_name='Costo Unitario')
    
#     def __str__(self):
#         return self.nombre

#     def toJSON(self):
#         item = model_to_dict(self)
#         item['thumbnail'] = '{}{}'.format(MEDIA_URL, self.thumbnail)
#         return item
