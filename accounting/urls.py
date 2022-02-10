from django.urls import path
from .views import ReportSaleView, ReportPurchaseView

urlpatterns = [
    path('report/sales', ReportSaleView.as_view(), name='ReportSaleView'),
    path('report/purchase', ReportPurchaseView.as_view(), name='ReportPurchaseView'),
]
