from django.urls import path
from .views import ReportSaleView

urlpatterns = [
    path('reports/', ReportSaleView.as_view(), name='ReportSaleView'),

]
