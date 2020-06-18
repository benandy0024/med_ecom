from django.contrib import admin
from django.conf.urls import url
from.views import SaleView,SaleViewAjax

urlpatterns = [
    url(r'^sales/$', SaleView.as_view(),name='sales'),
    url(r'^sales/data$', SaleViewAjax.as_view(), name='sales-data'),

]