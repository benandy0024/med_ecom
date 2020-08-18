"""Ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from.views import index
from products.views import category
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name='main_home'),
    path('category',category ,name='category'),
    path('account/', include(("accounts.urls",'accounts'),namespace='accounts')),

    path('analytic/', include(("analytics.urls", 'analytics'), namespace='analytics')),
    path('order/', include(("Orders.urls",'Orders'),namespace='Orders')),
    path('carts/', include(("carts.urls",'carts'),namespace='carts')),
    path('products/', include(("products.urls",'products'),namespace='products')),
    path('payment/', include(("Payments.urls", 'Payments'), namespace='Payments')),
    path('admin_panel/', include(("administration.urls",'administration'),namespace='administration')),
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

