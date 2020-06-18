from django.conf.urls import url
from . import views

urlpatterns = [
    url('home/', views.index, name="home"),
   url('charge/', views.charge, name="charge"),
    url('success/', views.successMsg, name="success"),
    # url('checkout/', views.checkout, name="checkout"),
]
