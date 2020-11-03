from django.urls import reverse_lazy
from django.http import JsonResponse
from gestion.mixins import ValidatePermissionRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from inventario.models import ProdServ
from inventario.forms import ProdServForm

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
                art.cantidad_almacen = request.POST['cantidad_almacen']
                art.save()
            elif action == 'edit':
                art = ProdServ.objects.get(pk=request.POST['id'])
                art.nombre = request.POST['nombre']
                art.categoria = request.POST['categoria']
                art.thumbnail = request.POST['thumbnail']
                art.precio = request.POST['precio']
                art.costo = request.POST['costo']
                art.cantidad_almacen = request.POST['cantidad_almacen']
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

class ServiceListView(TemplateView):
    permission_required = ('clients.view_cliente', 'clients.change_cliente')
    url_redirect = reverse_lazy('CashRegister')
    # model = Producto
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
                for i in ProdServ.objects.filter(categoria='S'):
                    data.append(i.toJSON())
            elif action == 'add':
                art = ProdServ()
                art.nombre = request.POST['nombre']
                art.categoria = request.POST['categoria']
                art.thumbnail = request.POST['thumbnail']
                art.precio = request.POST['precio']
                art.costo = request.POST['costo']
                art.save()
            elif action == 'edit':
                art = ProdServ.objects.get(pk=request.POST['id'])
                art.nombre = request.POST['nombre']
                art.categoria = request.POST['categoria']
                art.thumbnail = request.POST['thumbnail']
                art.precio = request.POST['precio']
                art.costo = request.POST['costo']
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