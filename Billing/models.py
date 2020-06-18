from django.db import models
from accounts.models import GuestEmail
from django.db import models
from  core.models import User
from  django.db.models.signals import post_save,pre_save
import stripe
# Create your models here.
stripe.api_key="sk_test_HBJfc8IKGbe6DDjcIA2Jl8P900NGSbqtBI"

# Create your models here.
class BillingProfileManager(models.Manager):
    def new_or_get(self,request):
        user=request.user
        guest_email_id = request.session.get('guest_email_id')
        created=False
        obj=None
        if user.is_authenticated:
            # logged in user checkout ;remember payement stuff
            obj, created=self.model.objects.get_or_create(
                user=user, email=user.email
            )
        elif guest_email_id is not None:
            # logged in user checkout, auto reload  payement stuff
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = BillingProfile.objects.get_or_create(
                email=guest_email_obj.email)
        else:
            pass
        return obj,created



class Customer(models.Model):
    name=models.CharField(max_length=120,null=True,blank=True)
    email = models.EmailField()
    customer_id = models.CharField(max_length=120, null=True, blank=True)


    def __str__(self):
        return self.name
class BillingProfile(models.Model):
    user=models.OneToOneField(User,unique=True,null=True,blank=True,on_delete='CASCADE')

    email=models.EmailField()
    active=models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id=models.CharField(max_length=120,null=True,blank=True)
    objects=BillingProfileManager()

    def __str__(self):
        return self.email
    def get_card(self):
        return self.card_set.all()
    @property
    def has_card(self):
        card_qs=self.get_card()
        return card_qs.exists()

    @property
    def default_card(self):
        default_cards=self.get_card().filter(default=True)
        if default_cards.exists():
            return default_cards.first()
        return None


def user_creaeted_receiver(sender,instance,created,*args,**kwargs):
    if created and instance.email :
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)
post_save.connect(user_creaeted_receiver,sender=User)

class Card(models.Model):
    billing_profile=models.ForeignKey(BillingProfile,on_delete='CASCADE')
    stripe_id=models.CharField(max_length=120,null=True,blank=True)
    brand=models.CharField(max_length=120,null=True,blank=True)
    country=models.CharField(max_length=20,null=True,blank=True)
    exp_month=models.IntegerField()
    exp_year=models.IntegerField()
    last4=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return "{} {}".format(self.brand,self.last4)

class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete='CASCADE')
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    paid= models.BooleanField(default=False)
    refunded=models.BooleanField(default=False)
    outcome= models.TextField(max_length=20,null=True,blank=True)
    outcome_type=models.CharField(max_length=20,null=True,blank=True)
    seller_message=models.CharField(max_length=20,null=True,blank=True)
    risk_level=models.CharField(max_length=20,null=True,blank=True)
    # objects=ChargeManager()
