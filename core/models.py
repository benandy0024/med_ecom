from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from  django.db.models.signals import post_save,pre_save
import stripe
# Create your models here.
class User(AbstractUser):
    customer_id=models.CharField(max_length=120,default=False)
    active=models.BooleanField(default=True)



def billing_profile_created_receiver(sender,instance,*args,**kwargs):
    if not instance.customer_id and instance.email :
        print("Actual api request send to stripe/braintree")
        customer=stripe.Customer.create(
            email=instance.email,
            name=instance.username


        )
        print("stripr",customer)
        instance.customer_id=customer.id
pre_save.connect(billing_profile_created_receiver,sender=User)


class UserComment(models.Model):
    name=models.CharField(max_length=120)
    contact = models.CharField(max_length=120,default=None)
    pharmacy_name = models.CharField(max_length=120,default=None)
    email = models.EmailField(max_length=120)
    comment = models.TextField(max_length=120)
    def __str__(self):
        return self.name