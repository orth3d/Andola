from unicodedata import name
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Sum, Q
from django.db.models.functions import Coalesce
from datetime import datetime
from .forms import ReportForm
from gestion.models import Sale, DetSale, Purchase, DetPurchase
from gestion.mixins import ValidatePermissionRequiredMixin
from inventario.models import ProdServ
import json
# Create your views here.

class ReportSaleView(ValidatePermissionRequiredMixin, TemplateView):
    permission_required = ('gestion.view_Venta')
    url_redirect = reverse_lazy('CashRegister')
    template_name= 'accounting/report.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                terapeuta = request.POST.get('terapeuta', '')
                search = Sale.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                    if len(terapeuta):
                        search = search.filter(added=terapeuta)
                for s in search:
                    data.append([
                        s.id,
                        s.cli.nombre + ' ' + s.cli.apellido,
                        s.date_joined.strftime('%Y-%m-%d'),
                        s.added.username,
                        format(s.total, '.2f'),
                        format(s.costo, '.2f'),
                        format(s.total-s.costo, '.2f'),
                        ' ',
                    ])
                total = search.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
                costo = search.aggregate(t=Coalesce(Sum('costo'), 0)).get('t')
                utilidad = total-costo
                data.append([
                    '---',
                    '---',
                    '---',
                    '---',
                    format(total, '.2f'),
                    format(costo, '.2f'),
                    format(utilidad, '.2f'),
                    ' ',
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de ventas'
        context['list_url'] = reverse_lazy('ReportSaleView')
        context['form'] = ReportForm()
        return context
    
class ReportPurchaseView(ValidatePermissionRequiredMixin, TemplateView):
    permission_required = ('gestion.view_Compra')
    url_redirect = reverse_lazy('PurchaseRegister')
    template_name= 'accounting/report_purchase.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = Purchase.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.proveedor.nombre,
                        s.date_joined.strftime('%Y-%m-%d'),
                        format(s.total, '.2f'),
                        ' ',
                    ])
                total = search.aggregate(r=Coalesce(Sum('total'), 0)).get('r')

                data.append([
                    '---',
                    '---',
                    '---',
                    format(total, '.2f'),
                    ' ',
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Compras y Pagos'
        context['list_url'] = reverse_lazy('ReportPurchaseView')
        context['form'] = ReportForm()
        return context

class DashboardView(TemplateView):
    
    def get_template_names(self):
        if self.request.user.is_staff:  # a certain check
            return ['accounting/dashboard.html']
        else:
            return ['accounting/dash_employees.html']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_sales_year_month':
                data = self.get_graph_sales_year_month()
            elif action == 'get_graph_purchase_year_month':
                data = self.get_graph_purchase_year_month()
            elif action == 'get_graph_sales_last_year_month':
                data = self.get_graph_sales_last_year_month()
            elif action == 'get_graph_sales_product_month':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.get_graph_sales_product_month(),
                }
            elif action == 'get_graph_sales_service_month':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.get_graph_sales_service_month(),
                }
            elif action == 'get_graph_sales_product_year':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.get_graph_sales_product_year(),
                }
            elif action == 'get_graph_sales_service_year':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.get_graph_sales_service_year(),
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_graph_sales_year_month(self):
        data = {'total':[], 'gasto':[], 'utilidad':[], 'totAnual':[], 'gasAnual':[], 'utiAnual':[]}
        try:
            year = datetime.now().year
            totalAnual = Sale.objects.filter(date_joined__year= year).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
            data['totAnual'] = float(totalAnual)
            gastoAnual = Sale.objects.filter(date_joined__year= year).aggregate(r=Coalesce(Sum('costo'), 0)).get('r')
            data['gasAnual'] = float(gastoAnual)
            utiAnual = totalAnual - gastoAnual
            data['utiAnual'] = float(utiAnual)
            # Ventas por mes
            for m in range(1, 13):
                total = Sale.objects.filter(date_joined__year= year, date_joined__month=m).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
                data['total'].append(float(total))
                gasto = Sale.objects.filter(date_joined__year= year, date_joined__month=m).aggregate(g=Coalesce(Sum('costo'), 0)).get('g')
                data['gasto'].append(float(gasto))
                utilidad = total - gasto
                data['utilidad'].append(float(utilidad))

        except:
            pass
        return data

    def get_graph_purchase_year_month(self):
        data = {'total':[], 'totAnual':[]}
        try:
            year = datetime.now().year
            totalAnual = Purchase.objects.filter(date_joined__year= year).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
            data['totAnual'] = float(totalAnual)
            # Ventas por mes
            for m in range(1, 13):
                total = Purchase.objects.filter(date_joined__year= year, date_joined__month=m).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
                data['total'].append(float(total))
            print(data)
        except:
            pass
        return data
    
    def get_graph_sales_last_year_month(self):
        data = {'total':[], 'gasto':[], 'utilidad':[], 'totAnual':[], 'gasAnual':[], 'utiAnual':[]}
        try:
            year = datetime.now().year
            year = year-1
            totalAnual = Sale.objects.filter(date_joined__year= year).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
            data['totAnual'] = float(totalAnual)
            gastoAnual = Sale.objects.filter(date_joined__year= year).aggregate(r=Coalesce(Sum('costo'), 0)).get('r')
            data['gasAnual'] = float(gastoAnual)
            utiAnual = totalAnual - gastoAnual
            data['utiAnual'] = float(utiAnual)
            # Ventas por mes
            for m in range(1, 13):
                total = Sale.objects.filter(date_joined__year= year, date_joined__month=m).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
                data['total'].append(float(total))
                gasto = Sale.objects.filter(date_joined__year= year, date_joined__month=m).aggregate(g=Coalesce(Sum('costo'), 0)).get('g')
                data['gasto'].append(float(gasto))
                utilidad = total - gasto
                data['utilidad'].append(float(utilidad))

        except:
            pass
        return data

    def get_graph_sales_product_month(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for p in ProdServ.objects.filter(categoria='P'):
                total = DetSale.objects.filter(sale__date_joined__year= year, sale__date_joined__month=month, prod_id=p.id).aggregate(
                    r=Coalesce(Sum('subtotal'), 0)).get('r')
                if total > 0:
                    data.append({
                        'name': p.nombre,
                        'y': float(total)
                    })
        except:
            pass
        return data

    def get_graph_sales_service_month(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for p in ProdServ.objects.filter(categoria='S'):
                total = DetSale.objects.filter(sale__date_joined__year= year, sale__date_joined__month=month, prod_id=p.id).aggregate(
                    r=Coalesce(Sum('subtotal'), 0)).get('r')
                if total > 0:
                    data.append({
                        'name': p.nombre,
                        'y': float(total)
                    })
        except:
            pass
        return data

    def get_graph_sales_product_year(self):
        data = []
        year = datetime.now().year
        try:
            for p in ProdServ.objects.filter(categoria='P'):
                total = DetSale.objects.filter(sale__date_joined__year= year, prod_id=p.id).aggregate(
                    r=Coalesce(Sum('cant'), 0)).get('r')
                if total > 0:
                    data.append({
                        'name': p.nombre,
                        'y': float(total)
                    })
        except:
            pass
        return data

    def get_graph_sales_service_year(self):
        data = []
        year = datetime.now().year
        try:
            for p in ProdServ.objects.filter(categoria='S'):
                total = DetSale.objects.filter(sale__date_joined__year= year, prod_id=p.id).aggregate(
                    r=Coalesce(Sum('cant'), 0)).get('r')
                if total > 0:
                    data.append({
                        'name': p.nombre,
                        'y': float(total)
                    })
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        context['graph_purchase_year_month'] = self.get_graph_purchase_year_month()
        context['graph_sales_last_year_month'] = self.get_graph_sales_last_year_month()
        return context
 
