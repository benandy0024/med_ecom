from django.contrib import admin
from django.conf.urls import url
from.views import payment_method_view,charge,successMsg

urlpatterns = [
 url('payment_method', payment_method_view, name='payment_method_view'),
 # url('payment/create/', payment_method_create_view, name='payment_method_view_endpoint'),
 #    url('home', index, name="index"),
    url('payment/', charge, name="charge"),
    url('success/', successMsg, name="success"),
    #
    # url('payment-method/create', payment_method_create_view, name='payment_method_view_endpoint'),

]