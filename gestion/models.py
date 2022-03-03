# import json
# from itertools import chain
from ast import Delete
from django.db import models
from django.forms import model_to_dict
from clients.models import Cliente
from datetime import datetime
from inventario.models import ProdServ, Proveedor, Articulo
from django.contrib.auth.models import User

class Sale(models.Model):
    cli = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    costo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    comment = models.CharField(verbose_name='Comentarios', unique=False, blank=True, max_length=200)
    added = models.ForeignKey(User, default=1, on_delete=models.SET(1), null=False, verbose_name='Agregado por')

    def __str__(self):
        return self.cli.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['costo'] = format(self.costo, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        item['comment'] = self.comment
        item['added'] = self.added.username
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detsale_set.all():
            det.prod.stock += det.cant
            det.prod.save()
        super(Sale, self).delete()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(ProdServ, on_delete=models.SET(1))
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subcosto = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subcosto'] = format(self.subcosto, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']

class Purchase(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    comment = models.CharField(verbose_name='Comentarios', unique=False, blank=True, max_length=200)
    added = models.ForeignKey(User, default=1, on_delete=models.SET(1), null=False, verbose_name='Agregado por')

    def __str__(self):
        return self.proveedor.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['proveedor'] = self.proveedor.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['total'] = format(self.total, '.2f')
        item['det'] = [i.toJSON() for i in self.detpurchase_set.all()]
        item['comment'] = self.comment
        item['added'] = self.added.username
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detpurchase_set.all():
            det.artic.stock -= det.cant
            det.artic.save()
        super(Purchase, self).delete()

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['id']


class DetPurchase(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    artic = models.ForeignKey(Articulo, on_delete=models.SET(1))
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.artic.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['artic'] = self.artic.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compras'
        ordering = ['id']