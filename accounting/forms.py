from django.forms import *
from django.contrib.auth.models import User

class ReportForm(Form):
    date_range = CharField(widget=TextInput(attrs= {
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    terapeuta = ModelChoiceField(User.objects.all(), widget=Select(attrs= {
        'class': 'form-control',
        'placeholder': 'Terapeuta'
    }))