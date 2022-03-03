from django.urls import reverse_lazy
from django.http import JsonResponse
from gestion.mixins import ValidatePermissionRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from inventario.models import ProdServ, Proveedor, Articulo
from inventario.forms import ProdServForm, proveedorForm, ArticuloForm

# Create your views here.
class ProductListView(TemplateView):
    url_redirect = reverse_lazy('CashRegister')
    # model = Producto
    template_name = 'inventario/products_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in ProdServ.objects.filter(categoria='P'):
                    data.append(i.toJSON())
            elif action == 'add':
                art = ProdServ()
                art.nombre = request.POST['nombre']
                art.categoria = request.POST['categoria']
                art.thumbnail = request.POST['thumbnail']
                art.precio = request.POST['precio']
                art.costo = request.POST['costo']
                art.stock = request.POST['stock']
                art.save()
            elif action == 'edit':
                art = ProdServ.objects.get(pk=request.POST['id'])
                art.nombre = request.POST['nombre']
                art.categoria = request.POST['categoria']
                # art.thumbnail = request.POST['thumbnail']
                art.precio = request.POST['precio']
                art.costo = request.POST['costo']
                art.stock = request.POST['stock']
                art.save()
            elif action =='delete':
                art = ProdServ.objects.get(pk=request.POST['id'])
                art.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de productos'
        # context['create_url'] = reverse_lazy('product_create')
        context['list_url'] = reverse_lazy('ProductListView')
        context['entity'] = 'Productos'
        context['form'] = ProdServForm()
        return context

class ArticlesListView(TemplateView):
    # permission_required = ('clients.view_cliente', 'clients.change_cliente')
    url_redirect = reverse_lazy('PurchaseRegister')
    template_name = 'inventario/services_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Articulo.objects.filter(categoria='A'):
                    data.append(i.toJSON())
            elif action == 'add':
                art = Articulo()
                art.nombre = request.POST['nombre']
                art.categoria = request.POST['categoria']
                art.precio = request.POST['precio']
                art.descripcion = request.POST['descripcion']
                art.stock = request.POST['stock']
                art.save()
            elif action == 'edit':
                art = Articulo.objects.get(pk=request.POST['id'])
                art.nombre = request.POST['nombre']
                art.categoria = request.POST['categoria']
                art.precio = request.POST['precio']
                art.descripcion = request.POST['descripcion']
                art.stock = request.POST['stock']
                art.save()
            elif action =='delete':
                art = Articulo.objects.get(pk=request.POST['id'])
                art.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de articulos'
        context['list_url'] = reverse_lazy('ArticlesListView')
        context['entity'] = 'Articulos'
        context['form'] = ArticuloForm()
        return context

class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = proveedorForm
    template_name = 'gestion/prov_create.html'
    success_url = reverse_lazy('ProveedoresListView')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # if action == 'search_categoria_id':
            #     data = []
                # for i in SubCategoryProv.objects.filter(categoria_id=request.POST['id']):
                    # data.append({'id': i.id, 'name': i.name})
            if action == 'add':
                form = self.get_form()
                data = form.save(commit=False)
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear nuevo Proveedor'
        context['entity'] = 'Proveedor'
        context['list_url'] = self.success_url # reverse_lazy('ProveedoresListView')
        context['action'] = 'add'
        return context

class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = proveedorForm
    template_name = 'gestion/prov_create.html'
    success_url = reverse_lazy('ProveedoresListView')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Proveedor'
        context['entity'] = 'Proveedor'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context