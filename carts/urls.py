from django.contrib import admin
from django.conf.urls import url
from.views import cart_home,cart_update,checkout_home,checkout_done_view

urlpatterns = [
    url(r'^$', cart_home,name='cart_view'),
 url(r'^checkout',checkout_home,name='checkout'),
url('(?P<slug>[\w-]+)/$',cart_update,name='update'),
url(r'^success',checkout_done_view,name='success'),
# url('update/(?P<qty>\d+)/$',cart_update,name='update'),

]