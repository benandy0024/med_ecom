import math
import datetime
from django.db import models
from carts.models import Cart,CartItem
from Ecom.utils import unique_order_id_generator
from django.db.models.signals import post_save,pre_save
from django.db.models import Sum,Avg,Count
from django.urls import reverse
from django.utils import timezone
from Billing.models import BillingProfile
from core.models import User
# Create your models here.

ORDER_STATUS_CHOICES=(
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded'),
)

class OrderManagerQuerySet(models.query.QuerySet):
    def get_sales_breakdown(self):
        recent=self.recent()
        recent_data=recent.total_data()
        recent_cart_data=recent.cart_data()
        paid=recent.by_status(status='paid')
        paid_data=recent.total_data()
        data={
           'recent':recent,
            'recent_cart_data':recent_cart_data,
            'recent_data':recent_data,
            'paid':paid,
            'paid_data':paid_data

        }

        return data
    def recent(self):
        return self.order_by("-timestamp")

    def by_range(self,start_date,end_date=None):
        if end_date is None:
            return self.filter(timestamp__gte=start_date)
        return self.filter(timestamp__gte=start_date).filter(timestamp__lte=end_date)
    def by_weeks_range(self,weeks_ago=1,numbers_of_weeks=1):
        if numbers_of_weeks>weeks_ago:
            numbers_of_weeks=weeks_ago
        days_ago_start=weeks_ago*7
        days_ago_end=days_ago_start-(numbers_of_weeks*7)
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end)
        return self.by_range(start_date,end_date=end_date)
    def by_date(self):
        now=timezone
        return self.filter(timestamp__day= now().day
)
    def total_data(self):
        return self.aggregate( Sum("total"),Avg("total"),)
    def cart_data(self):
        return self.aggregate(
            Sum("cart__cartitem__products__price"),
            Avg("cart__cartitem__products__price"),
            Count("cart__cartitem__products"))
    def by_status(self,status='paid'):
        return self.filter(status=status)
    def by_request(self,request):
        billing_profile,created=BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model,using=self.db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)
    def new_or_get(self,billing_profile,cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True,
            status='created',
                                       )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj=self.model.objects.create(
                billing_profile=billing_profile,
                cart=cart_obj)
            created=True
        return obj, created
class Order(models.Model):
    user = models.ForeignKey(User, on_delete='CASCADE', null=True, blank=True)
    billing_profile=models.ForeignKey(BillingProfile,on_delete='CASCADE',null=True,blank=True)
    order_id=models.CharField(max_length=120,blank=True)
    cart=models.ForeignKey(Cart,on_delete='CASCADE')
    cart_item = models.ForeignKey(CartItem, on_delete='CASCADE',null=True,blank=True)
    status=models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active=models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=True,)
    objects=OrderManager()
    def __str__(self):
        return self.order_id
        # url
    def get_absolute_url(self):
        # return '/products/{slug}/'.format(slug=self.slug)
        return reverse('Orders:order_detail', kwargs={"order_id": self.order_id})

    def update_total(self):
        cart_total = self.cart.total
        new_total = math.fsum([cart_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total
    def check_done(self):
        billing_profile=self.billing_profile
        total=self.total
        if billing_profile and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status="paid"
            self.save()
        return self.status

def pre_save_create_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id=unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)
pre_save.connect(pre_save_create_order_id,sender=Order)


def post_save_cart_total(sender,instance,*args,**kwargs):

    cart_obj=instance
    cart_total=cart_obj.total
    cart_id=cart_obj.id
    qs=Order.objects.filter(cart__id=cart_id)
    if qs.count()==1:
        order_obj=qs.first()
        order_obj.update_total()
post_save.connect(post_save_cart_total,sender=Cart)

def post_save_order(sender,created,instance,*args,**kwargs):
    print('running')
    if created:
        print('updated...first')
        instance.update_total()
post_save.connect(post_save_order, sender=Order)