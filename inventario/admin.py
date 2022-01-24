from django.contrib import admin
from .models import Articulo, ProdServ, Proveedor

# Register your models here.
admin.site.register(ProdServ)
admin.site.register(Proveedor)
admin.site.register(Articulo)
