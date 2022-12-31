from unicodedata import name
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
# from AnDjo.inventario.models import Articulo
from posts.models import Post
from clients.models import Cliente
from clients.forms import clientForm
from inventario.forms import proveedorForm, ArticuloForm
from inventario.models import ProdServ, Proveedor, Articulo
from gestion.models import Sale, DetSale, Purchase, DetPurchase
from .forms import SaleForm, PurchaseForm
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.contrib import messages

from django.db.models import Value as V
from django.db.models.functions import Concat


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
            elif action =='add':
                prov = Proveedor()
                prov.nombre = request.POST['nombre']
                prov.categoria = request.POST['categoria']
                prov.tel1 = request.POST['tel1']
                prov.tel2 = request.POST['tel2']
                prov.mail = request.POST['mail']
                prov.address = request.POST['address']
                prov.website = request.POST['website']
                prov.location = request.POST['location']
                prov.keywords = request.POST['keywords']
                prov.save()
            elif action =='edit':
                prov = Proveedor.objects.get(pk=request.POST['id'])
                prov.nombre = request.POST['nombre']
                prov.categoria = request.POST['categoria']
                prov.tel1 = request.POST['tel1']
                prov.tel2 = request.POST['tel2']
                prov.mail = request.POST['mail']
                prov.address = request.POST['address']
                prov.website = request.POST['website']
                prov.location = request.POST['location']
                prov.keywords = request.POST['keywords']
                prov.save()
            elif action =='delete':
                prov = Proveedor.objects.get(pk=request.POST['id'])
                prov.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proveedores'
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
                    sale.added_id = vents['added'] #request.user
                    sale.save()

                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        det.prod.stock -= det.cant
                        det.prod.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                #clies = Cliente.objects.filter(Q(nombre__icontains=term) | Q(apellido__icontains=term))[0:10]
                clies = Cliente.objects.annotate(full_name=Concat('nombre', V(' '), 'apellido')).\
                    filter(full_name__icontains=term)[0:20]
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
        context['productos'] = self.products.filter(categoria='P', stock__gt=0).order_by('nombre')
        context['servicios'] = self.products.filter(categoria='S').order_by('nombre')
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
                # if request.user.is_staff:
                    # for i in Sale.objects.all():#filter(added__isnull=False):
                        # data.append(i.toJSON())
                # else:
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
                        det.prod.stock -= det.cant
                        det.prod.save()
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

class PurchaseRegister(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'gestion/compra.html'
    success_url = reverse_lazy('PurchaseRegister')
    url_redirect = success_url
    products = Articulo.objects.all()
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    purch = Purchase()
                    purch.date_joined = vents['date_joined']
                    purch.proveedor_id = vents['provee']
                    purch.total = float(vents['total'])
                    purch.comment = vents['comment']
                    purch.added = request.user
                    purch.save()

                    for i in vents['products']:
                        det = DetPurchase()
                        det.purchase_id = purch.id
                        det.artic_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        det.artic.stock += det.cant
                        det.artic.save()
                    data = {'id': purch.id}
                print(data)
            elif action == 'search_articulo':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term']
                articulo = Articulo.objects.filter(Q(nombre__icontains=term))
                for i in articulo.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'create_articulo':
                with transaction.atomic():
                    frmArticulo = ArticuloForm(request.POST)
                    data = frmArticulo.save()
                    print(data)
            elif action == 'search_proveedor':
                data = []
                term = request.POST['term']
                provee = Proveedor.objects.filter(Q(nombre__icontains=term))[0:10]
                print(provee)
                for i in provee:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'create_proveedor':
                with transaction.atomic():
                    frmProveedor = proveedorForm(request.POST)
                    data = frmProveedor.save()
                    print(data)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulos'] = self.products.all()
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['fecha'] = date.today()
        context['det'] = []
        context['frmProveedor'] = proveedorForm()
        context['frmArticulo'] = ArticuloForm()
        return context

class PurchaseListView(ListView):
    model = Purchase
    template_name = 'gestion/purchase_list.html'

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
                    for i in Purchase.objects.all():#filter(added__isnull=False):
                        data.append(i.toJSON())
                else:
                    for i in Purchase.objects.filter(date_joined=datetime.now()):
                        data.append(i.toJSON())
            elif action == 'search_details_art':
                data = []
                for i in DetPurchase.objects.filter(purchase_id=request.POST['id']):
                   data.append(i.toJSON())
            elif action =='delete':
                if request.user.is_staff:
                    art = Purchase.objects.get(pk=request.POST['id'])
                    art.delete()
                else:
                    data['error'] = 'Solicite autorización para eliminar compra'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['create_url'] = reverse_lazy('PurchaseRegister')
        context['list_url'] = reverse_lazy('PurchaseListView')
        context['entity'] = 'Compras'
        return context

class PurchaseUpdateView(UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'gestion/compra.html'
    success_url = reverse_lazy('PurchaseListView')
    url_redirect = success_url
    products = Articulo.objects.all()
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    purch = self.get_object()
                    purch.date_joined = vents['date_joined']
                    purch.proveedor_id = vents['provee']
                    purch.total = float(vents['total'])
                    purch.comment = vents['comment']
                    purch.added = request.user
                    purch.save()
                    purch.detpurchase_set.all().delete()

                    for i in vents['products']:
                        det = DetPurchase()
                        det.purchase_id = purch.id
                        det.artic_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.artic.stock += det.cant
                        det.artic.save()
                        det.save()
                    data = {'id': purch.id}
            elif action == 'search_articulo':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term']
                articulo = Articulo.objects.filter(Q(nombre__icontains=term))
                for i in articulo.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'create_articulo':
                with transaction.atomic():
                    frmArticulo = ArticuloForm(request.POST)
                    data = frmArticulo.save()
                    print(data)
            elif action == 'search_proveedor':
                data = []
                term = request.POST['term']
                provee = Proveedor.objects.filter(Q(nombre__icontains=term))[0:10]
                print(provee)
                for i in provee:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'create_proveedor':
                with transaction.atomic():
                    frmProveedor = proveedorForm(request.POST)
                    data = frmProveedor.save()
                    print(data)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_product_details(self):
        data = []
        try:
            for i in DetPurchase.objects.filter(purchase_id=self.get_object().id):
                item = i.artic.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulos'] = self.products.all()
        context['title'] = 'Editar gasto'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_product_details())
        context['frmProveedor'] = proveedorForm()
        context['frmArticulo'] = ArticuloForm()
        return context