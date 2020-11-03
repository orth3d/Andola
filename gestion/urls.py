from django.urls import path
from .views import BlogListView, ClientsListView, ClientAddView, ClientFormView, CashRegister, SaleListView, SaleUpdateView, SaleInvoicePdfView
from accounting.views import DashboardView
from posts.views import PostCreateView, PostUpdateView, PostDeleteView
from inventario.views import ProductListView, ServiceListView

urlpatterns = [
    path('', DashboardView.as_view(), name='DashboardView'),
    path('clients/', ClientsListView.as_view(), name='ClientsListView'),
    path('clients/create/', ClientAddView.as_view(), name='client_create'),
    path('clients/form/', ClientFormView.as_view(), name='client_form'),
    path('blog/', BlogListView.as_view(), name='BlogListView'),
    path('blog/create/', PostCreateView.as_view(), name='post_create'),
    path('blog/edit/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('blog/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('productos/', ProductListView.as_view(), name='ProductListView'),
    path('servicios/', ServiceListView.as_view(), name='ServiceListView'),
    path('caja/', CashRegister.as_view(), name='CashRegister'),
    path('sales/', SaleListView.as_view(), name='SaleListView'),
    path('sales/update/<int:pk>/', SaleUpdateView.as_view(), name='SaleUpdateView'),
    path('sales/invoice/<int:pk>/', SaleInvoicePdfView.as_view(), name='SaleInvoicePDF'),
]
