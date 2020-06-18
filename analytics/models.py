from django.db import models
from django.db.models.signals import post_save,pre_save
from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from accounts.signals import user_logged_in
from .signals import object_viewed_signal
from .utils import get_client_ip
User=settings.AUTH_USER_MODEL
# Create your models here.
class ObjectViewedQuerySet(models.query.QuerySet):
    def by_model(self,model_class,model_queryset=False):
        c_type=ContentType.objects.get_for_model(model_class)
        qs=self.filter(content_type=c_type)
        if model_queryset:
            viewed_ids=[x.object_id for x in qs]
            return model_class.objects.filter(pk__in=viewed_ids)
        return qs
class ObjectViewedManager(models.Manager):
    def get_queryset(self):
        return ObjectViewedQuerySet(self.model,using=self.db)
    def by_model(self,model_class,model_queryset):
        return self.get_queryset().by_model(model_class,model_queryset=model_queryset)

class ObjectViewed(models.Model):
    user=models.ForeignKey(User,blank=True,null=True,on_delete='CASCADE')#User instance instance.id
    ip_address=models.CharField(max_length=220,blank=True,null=True)#IP FIELD
    content_type=models.ForeignKey(ContentType,on_delete='CASCADE')# User Product Order Cart Address
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')#Product instance
    timestamp=models.DateTimeField(auto_now_add=True)
    objects=ObjectViewedManager()
    def __str__(self):
        return "%s viewed %s" %(self.content_object,self.timestamp)

    class Meta:
        ordering=['-timestamp']# most recent saved show up first
        verbose_name='Object viewed'
        verbose_name_plural='Object viewed'
def object_viewed_receiver(sender,instance,request,*args,**kwargs):
    c_type=ContentType.objects.get_for_model(sender)#instance.__class__
    # print(sender)
    # print(instance)
    # print(request)
    # print(request.user)
    new_view_obj=ObjectViewed.objects.create(
        user=request.user,
        content_type=c_type,
        object_id=instance.id,
        ip_address=get_client_ip(request)
    )
object_viewed_signal.connect(object_viewed_receiver)

#custome session model
class UserSession(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete='CASCADE')  # User instance instance.id
    ip_address = models.CharField(max_length=220, blank=True, null=True)  # IP FIELD
    session_key = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    ended=models.BooleanField(default=False)


def user_logged_in_receiver(sender,instance,request,*args,**kwargs):
    print(instance)
    user=instance
    ip_address = get_client_ip(request)
    session_key=request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )

user_logged_in.connect(user_logged_in_receiver)
