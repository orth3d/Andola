# import json
from django.db import models
from django.forms import model_to_dict
from datetime import date
#from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class Cliente(models.Model):
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('X', 'Otro'),
    )
    nombre = models.CharField(max_length=264, unique=False)
    apellido = models.CharField(max_length=264, unique=False)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15, unique=False, blank=False) #PhoneNumberField(null=False, blank=False, unique=True, default='+521')
    mail = models.EmailField(max_length=264, unique=False, default='', blank=True)
    rfc = models.CharField(max_length=264, unique=False, default='', blank=True)
    
    def __str__(self):
        return str(self.nombre + ' ' + self.apellido)

    def get_age(self):
        today = date.today()
        age =  today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return age

    def get_full_name(self):
        return '{} {} / {} años'.format(self.nombre, self.apellido, self.get_age())

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']
 
