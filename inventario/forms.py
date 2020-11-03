from django import forms
# from django.forms import TextInput, Textarea, Select, FileInput
from .models import ProdServ
# categoria = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

class ProdServForm(forms.ModelForm):

    class Meta:
        model = ProdServ
        fields = ('nombre', 'categoria', 'thumbnail', 'precio', 'costo', 'cantidad_almacen')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True


    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

# class ServiceForm(forms.ModelForm):

#     class Meta:
#         model = Servicio
#         fields = ('nombre', 'thumbnail', 'precio', 'costo')
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for form in self.visible_fields():
#             form.field.widget.attrs['class'] = 'form-control'
#             form.field.widget.attrs['autocomplete'] = 'off'
#         self.fields['nombre'].widget.attrs['autofocus'] = True
#         self.fields['thumbnail'].widget.attrs['accept'] = 'file/*'


#     def save(self, commit=True):
#         data = {}
#         form = super()
#         try:
#             if form.is_valid():
#                 form.save()
#             else:
#                 data['error'] = form.errors
#         except Exception as e:
#             data['error'] = str(e)
#         return data

