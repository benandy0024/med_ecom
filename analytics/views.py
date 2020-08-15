import datetime
import random
from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView,View
from django.db.models import Sum,Avg,Count
from Orders.models import Order
from django.utils import timezone
from django.http import JsonResponse,HttpResponse
from Orders.models import Order
from products.models import Product
# Create your views here.
class SaleViewAjax(View):
    def get(self,request, *args, **kwargs):
        data={}
        if request.user.is_staff:
            qs = Order.objects.all().by_weeks_range(weeks_ago=10, numbers_of_weeks=10)
            days=7
            startdate=timezone.now().today()-datetime.timedelta(days=days-1)
            datetime_list=[]
            labels=[]
            sales_item=[]
            for x in range(0,days):
                new_time=startdate+datetime.timedelta(days=x)
                datetime_list.append(new_time)
                labels.append(new_time.strftime("%a"))
                new_qs=qs.filter(timestamp__day=new_time.day,timestamp__month=new_time.month)
                day_total=new_qs.total_data()["total__sum"]or 0
                sales_item.append(day_total)
            if request.GET.get('type')=='week':
                data['labels'] = labels
                data['data']=sales_item
            if request.GET.get('type') == '4weeks':
                data['labels'] = ['4 weeks ago','3 weeks ago', '2 weeks ago', 'last weeks ', 'this week ago', ]
                current=5
                data['data']=[]
                for i in range(0,5):
                    new_qs=qs.by_weeks_range(weeks_ago=current,numbers_of_weeks=1)
                    sales_total=new_qs.total_data()["total__sum"]
                    if sales_total is None:
                        sales_total=0
                    data['data'].append(sales_total)
                    current-=1
        return JsonResponse(data)
class SaleView(TemplateView):
    template_name = 'analytics/analytics.html'
    def dispatch(self, request, *args, **kwargs):
        user=self.request.user
        if  not user.is_staff:
            return HttpResponse("not Allowed", status=402)
        return super(SaleView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self,*args, **kwargs):
        context=super(SaleView, self).get_context_data( *args, **kwargs)
        # two_weeks_ago=timezone.now()-datetime.timedelta(days=14)
        # one_weeks_ago = timezone.now() - datetime.timedelta(days=7)
        order_qs=Order.objects.count()
        product_qs = Product.objects.count()
        qs=Order.objects.all().by_weeks_range(weeks_ago=10,numbers_of_weeks=10)
        context["today"]=qs.by_range(start_date=timezone.now().date()).get_sales_breakdown()
        context["this_week"]=qs.by_weeks_range(weeks_ago=1,numbers_of_weeks=1).get_sales_breakdown()
        context["past_four_weeks"]=qs.by_weeks_range(weeks_ago=5,numbers_of_weeks=4).get_sales_breakdown()
        context['product_qs']=product_qs
        context['order_qs'] = order_qs


        return context
