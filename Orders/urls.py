from django.contrib import admin
from django.conf.urls import url,include
from.views import OrderListView,OrderDetailView

urlpatterns = [

    url(r'^$', OrderListView.as_view(), name='order_list'),
    url('(?P<order_id>[\w-]+)/$', OrderDetailView.as_view(), name='order_detail')
]