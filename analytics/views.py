import datetime
from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView,View
from django.db.models import Sum,Avg,Count
from Orders.models import Order
from django.utils import timezone
from django.http import JsonResponse,HttpResponse
# Create your views here.
class SaleViewAjax(View):
    def get(self,request, *args, **kwargs):
        data={}
        if request.user.is_staff:
            if request.GET.get('type')=='week':
                data['labels'] = ['Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                data['data']=[123,131,2302,12,323,313,4290]
            if request.GET.get('type') == '4weeks':
                data['labels'] = ['last week', 'one week ago', '2 weeks ago', '3 weeks ago', '4 weeks ago',]
                data['data'] = [123, 131, 2302, 12, 323]
        return JsonResponse(data)
class SaleView(TemplateView):
    template_name = 'analytics/sales.html'
    def dispatch(self, request, *args, **kwargs):
        user=self.request.user
        if  not user.is_staff:
            return HttpResponse("not Allowed", status=402)
        return super(SaleView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self,*args, **kwargs):
        context=super(SaleView, self).get_context_data( *args, **kwargs)
        # two_weeks_ago=timezone.now()-datetime.timedelta(days=14)
        # one_weeks_ago = timezone.now() - datetime.timedelta(days=7)
        qs=Order.objects.all().by_weeks_range(weeks_ago=10,numbers_of_weeks=10)
        context["today"]=qs.by_range(start_date=timezone.now().date()).get_sales_breakdown()
        context["this_week"]=qs.by_weeks_range(weeks_ago=1,numbers_of_weeks=1).get_sales_breakdown()
        context["past_four_weeks"]=qs.by_weeks_range(weeks_ago=5,numbers_of_weeks=4).get_sales_breakdown()


        return context
