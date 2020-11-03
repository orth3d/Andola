from django.urls import path
from .views import ReportSaleView

urlpatterns = [
    path('sale/', ReportSaleView.as_view(), name='ReportSaleView'),

]
