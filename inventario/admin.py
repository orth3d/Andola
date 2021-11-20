from django.contrib import admin
from .models import ProdServ, CategoryProv, Proveedor

# Register your models here.
admin.site.register(ProdServ)
admin.site.register(CategoryProv)
admin.site.register(Proveedor)
