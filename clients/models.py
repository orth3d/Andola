# import json
from django.db import models
from django.forms import model_to_dict
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

    def toJSON(self):
        item = model_to_dict(self)
        # item['telefono'] = json.dumps(str(Cliente.telefono))
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']
 
