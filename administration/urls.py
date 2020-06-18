from django.contrib import admin
from django.conf.urls import url
from.views import home,add_product,ProductListView,update,delete,view_order,order_detail
urlpatterns = [
    url(r'home/', home,name='home'),
    url(r'order/', view_order, name='view_order'),
      # url(r'index', index,name='home'),
    url(r'list',ProductListView.as_view(), name='list'),
    url(r'add', add_product, name='add'),
url(r'(?P<id>[\w-]+)$',order_detail, name='order-detail'),
url(r'update/(?P<slug>[\w-]+)/$', update, name='update'),
url(r'delete/(?P<slug>[\w-]+)/$', delete, name='delete'),

]