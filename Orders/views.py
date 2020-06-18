from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from Billing.models import BillingProfile
from.models import Order
# Create your views here.
class OrderListView(LoginRequiredMixin,ListView):
    def get_queryset(self):
        return Order.objects.by_request(self.request).order_by("-timestamp")
class OrderDetailView(LoginRequiredMixin,ListView):
    def get_object(self):
        qs=Order.objects.by_request(self.request
                                    ).filter(
            order_id=self.kwargs.get('order_id')
        )
        if qs.count()==1:
            return qs.first()
        raise Http404
    # def get_queryset(self):empl
    #     return Order.objects.by_request(self.request)

class OrderDetailView(LoginRequiredMixin,ListView):
    template_name = 'Orders/order_detail.html'
    def get_queryset(self):
        qs=Order.objects.by_request(self.request
                                    ).filter(
            order_id=self.kwargs.get('order_id')
        )
        if qs.count()==1:
            return qs.first()
        raise Http404


    # def get_queryset(self):
    #     return Order.objects.by_request(self.request)