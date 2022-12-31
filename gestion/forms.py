from django.forms import *
from inventario.models import ProdServ
from .models import Purchase, Sale
from clients.models import Cliente
from datetime import datetime
from django.contrib.auth.models import User


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['cli'].queryset = Cliente.objects.none()

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli' : Select(attrs={
                'autofocus': True,
                'autocomplete': 'off',
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'date_joined': DateInput(
                format='%Y-%m-%d', 
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#id_date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'total' : TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'comment' : TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'added' : Select(attrs= {
                'class': 'form-control'
            })
        }

class PurchaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Purchase
        fields = '__all__'
        widgets = {
            'proveedor' : Select(attrs={
                'autofocus': True,
                'autocomplete': 'off',
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'date_joined': DateInput(
                format='%Y-%m-%d', 
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#id_date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'total' : TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'comment' : TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off'
            })
        }