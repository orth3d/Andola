from django.urls import path
from .views import BlogListView, ClientsListView, CashRegister, SaleListView, SaleUpdateView, SaleInvoicePdfView, ProveedoresListView, PurchaseRegister, PurchaseListView, PurchaseUpdateView
from accounting.views import DashboardView
from posts.views import PostCreateView, PostUpdateView, PostDeleteView
from inventario.views import ProductListView, ArticlesListView, ProveedorCreateView, ProveedorUpdateView

urlpatterns = [
    path('', DashboardView.as_view(), name='DashboardView'),
    path('clients/', ClientsListView.as_view(), name='ClientsListView'),
    path('blog/', BlogListView.as_view(), name='BlogListView'),
    path('blog/create/', PostCreateView.as_view(), name='post_create'),
    path('blog/edit/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('blog/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('productos/', ProductListView.as_view(), name='ProductListView'),
    path('articulos/', ArticlesListView.as_view(), name='ArticlesListView'),
    path('proveedores/', ProveedoresListView.as_view(), name='ProveedoresListView'),
    path('proveedores/create/', ProveedorCreateView.as_view(), name='prov_create'),
    path('proveedores/edit/<int:pk>', ProveedorUpdateView.as_view(), name='prov_update'),
    path('caja/', CashRegister.as_view(), name='CashRegister'),
    path('sales/', SaleListView.as_view(), name='SaleListView'),
    path('sales/update/<int:pk>/', SaleUpdateView.as_view(), name='SaleUpdateView'),
    path('sales/invoice/<int:pk>/', SaleInvoicePdfView.as_view(), name='SaleInvoicePDF'),
    path('pagos/', PurchaseRegister.as_view(), name='PurchaseRegister'),
    path('pagos/update/<int:pk>/', PurchaseUpdateView.as_view(), name='PurchaseUpdateView'),
    path('salidas/', PurchaseListView.as_view(), name='PurchaseListView'),
]
