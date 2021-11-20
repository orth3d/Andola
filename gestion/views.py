from django.db import transaction
from django.db.models import Count, Q
# from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpRequest
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, FormView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from datetime import *
import json
from posts.models import Post
from clients.models import Cliente
from clients.forms import clientForm
from inventario.forms import proveedorForm
from inventario.models import ProdServ, Proveedor, CategoryProv # SubCategoryProv
from gestion.models import Sale, DetSale
from .forms import SaleForm
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.contrib import messages


def calculate_age(fecha_nacimiento):
    today = date.today()
    edad = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad   

class BlogListView(ListView):
    model = Post
    template_name = 'gestion/posts_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # data = Cliente.objects.get(pk=request.POST['id']).toJSON()
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Post.objects.all():
                    data.append(i.toJSON())   
            elif action =='delete':
                art = Post.objects.get(pk=request.POST['id'])
                art.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de publicaciones'
        context['create_url'] = reverse_lazy('post_create')
        context['list_url'] = reverse_lazy('BlogListView')
        context['entity'] = 'Posts'
        return context
   
class ClientsListView(TemplateView):
    template_name = 'gestion/clients_list.html'

    # @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Cliente.objects.all():
                    data.append(i.toJSON())
            elif action =='add':
                cli = Cliente()
                cli.nombre = request.POST['nombre']
                cli.apellido = request.POST['apellido']
                cli.genero = request.POST['genero']
                cli.fecha_nacimiento = request.POST['fecha_nacimiento']
                cli.telefono = request.POST['telefono']
                cli.mail = request.POST['mail']
                cli.rfc = request.POST['rfc']
                cli.save()
            elif action =='edit':
                cli = Cliente.objects.get(pk=request.POST['id'])
                cli.nombre = request.POST['nombre']
                cli.apellido = request.POST['apellido']
                cli.genero = request.POST['genero']
                cli.fecha_nacimiento = request.POST['fecha_nacimiento']
                cli.telefono = request.POST['telefono']
                cli.mail = request.POST['mail']
                cli.rfc = request.POST['rfc']
                cli.save()
            elif action =='delete':
                cli = Cliente.objects.get(pk=request.POST['id'])
                cli.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['list_url'] = reverse_lazy('erp:client')
        context['entity'] = 'Clientes'
        context['form'] = clientForm()
        return context

class ProveedoresListView(TemplateView):
    template_name = 'gestion/proveedores_list.html'
    # @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Proveedor.objects.all():
                    data.append(i.toJSON())
            # elif action =='add':
            #     prov = Proveedor()
            #     prov.nombre = request.POST['nombre']
            #     prov.categoria_id = request.POST['categoria']
            #     prov.subcategoria_id = request.POST['subcategoria']
            #     prov.tel1 = request.POST['tel1']
            #     prov.tel2 = request.POST['tel2']
            #     prov.mail = request.POST['mail']
            #     prov.address = request.POST['address']
            #     prov.website = request.POST['website']
            #     prov.location = request.POST['location']
            #     prov.save()
            # elif action =='edit':
            #     prov = Proveedor.objects.get(pk=request.POST['id'])
            #     prov.nombre = request.POST['nombre']
            #     prov.categoria = request.POST['categoria']
            #     prov.subcategoria = request.POST['subcategoria']
            #     prov.tel1 = request.POST['tel1']
            #     prov.tel2 = request.POST['tel2']
            #     prov.mail = request.POST['mail']
            #     prov.address = request.POST['address']
            #     prov.website = request.POST['website']
            #     prov.location = request.POST['location']
            #     prov.save()
            elif action =='delete':
                prov = Proveedor.objects.get(pk=request.POST['id'])
                prov.delete()
            elif action =='search_category_id':
                data = [{'id': '', 'text': '---------'}]
                # for i in SubCategoryProv.objects.filter(categoria_id=request.POST['id']):
                    # data.append({'id': i.id, 'text': i.name, 'data': i.categoria.toJSON()})
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proveedores'
        context['create_url'] = reverse_lazy('prov_create')
        context['list_url'] = reverse_lazy('gestion:proveedor')
        context['entity'] = 'Proveedores'
        context['form'] = proveedorForm()
        return context

class CashRegister(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'gestion/caja.html'
    success_url = reverse_lazy('CashRegister')
    url_redirect = success_url
    products = ProdServ.objects.all()
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'productos':
                data = []
                data = ProdServ.objects.get(pk=request.POST['id']).toJSON()
            elif action == 'servicios':
                data = []
                data = ProdServ.objects.get(pk=request.POST['id']).toJSON()
            if action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.total = float(vents['total'])
                    sale.costo = float(vents['costo'])
                    sale.comment = vents['comment']
                    sale.added = request.user
                    sale.save()

                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clies = Cliente.objects.filter(Q(nombre__icontains=term) | Q(apellido__icontains=term))[0:10]
                for i in clies:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    frmClient = clientForm(request.POST)
                    data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = self.products.filter(categoria='P')
        context['servicios'] = self.products.filter(categoria='S')
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['fecha'] = date.today()
        context['det'] = []
        context['frmClient'] = clientForm()
        return context

class SaleListView(ListView):
    model = Sale
    template_name = 'gestion/sales_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                if request.user.is_staff:
                    for i in Sale.objects.all():#filter(added__isnull=False):
                        data.append(i.toJSON())
                else:
                    for i in Sale.objects.filter(date_joined=datetime.now()):
                        data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                   data.append(i.toJSON())
            elif action =='delete':
                if request.user.is_staff:
                    art = Sale.objects.get(pk=request.POST['id'])
                    art.delete()
                else:
                    data['error'] = 'Solicite autorización para eliminar venta'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('CashRegister')
        context['list_url'] = reverse_lazy('SaleListView')
        context['entity'] = 'Ventas'
        return context

class SaleUpdateView(UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'gestion/caja.html'
    success_url = reverse_lazy('SaleListView')
    url_redirect = success_url
    products = ProdServ.objects.all()
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'productos':
                data = []
                data = ProdServ.objects.get(pk=request.POST['id']).toJSON()
            elif action == 'servicios':
                data = []
                data = ProdServ.objects.get(pk=request.POST['id']).toJSON()
            if action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = self.get_object()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.total = float(vents['total'])
                    sale.costo = float(vents['costo'])
                    sale.comment = vents['comment']
                    sale.save()
                    sale.detsale_set.all().delete()

                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clies = Cliente.objects.filter(Q(nombre__icontains=term) | Q(apellido__icontains=term))[0:10]
                for i in clies:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    frmClient = clientForm(request.POST)
                    data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_product_details(self):
        data = []
        try:
            for i in DetSale.objects.filter(sale_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context = {'productos': self.products, 'servicios': self.services,}
        context['productos'] = self.products.filter(categoria='P')
        context['servicios'] = self.products.filter(categoria='S')
        context['title'] = 'Editar venta'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_product_details())
        context['frmClient'] = clientForm()
        return context

class SaleInvoicePdfView(View):

    def link_callback(self, uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('gestion/invoice.html')
            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'ANDOLA SAS de CV', 'RFC': 'ASI180319S52', 'address': 'Nezahualcoyotl 45, Jajalpa Ecatepec 55090, Estado de México'},
                'icon': '{}{}'.format(settings.STATIC_DIR, '/img/logosq.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('SaleListView'))