from django import forms
# from django.forms import * # TextInput, Textarea, Select, FileInput
from .models import ProdServ, Proveedor, CategoryProv # SubCategoryProv
# 

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

class proveedorForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=CategoryProv.objects.all(), required=True, widget=forms.Select(attrs={
            'class': 'form-control select2'
        }))
    # subcategoria = forms.ModelChoiceField(queryset=SubCategoryProv.objects.none(), required=True, widget=forms.Select(attrs={
            # 'class': 'form-control select2'
        # }))
    class Meta:
        model = Proveedor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True
        self.fields['categoria'].widget.attrs['class'] = 'form-control select2'
        # self.fields['subcategoria'].widget.attrs['class'] = 'form-control select2'

        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data