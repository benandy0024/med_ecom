from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import is_safe_url
from Billing.models import BillingProfile,Customer
from carts.models import CartItem,Cart
from Orders.models import Order
from django.http import JsonResponse
from Billing.models import Card,Charge
import stripe
# Create your views here.
STRIPE_PUB_KEY='pk_test_QZinzyFakYCKsVwpJI0ttgBC00VIepUNf2'
stripe.api_key="sk_test_HBJfc8IKGbe6DDjcIA2Jl8P900NGSbqtBI"
def index(request):
    # if request.user.is_authenticated:
    # 	billing_profile=request.user.billingprofile
    # 	my_customer_id=billing_profile.customer_id
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if not billing_profile:
      return redirect("carts:cart_view")


    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url=next_

    return render(request, 'my_index.html',{"next_url":next_url})


def charge(request):
    if request.method=="POST":
        print(request.POST)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if request.user.is_authenticated:
            customer_id=request.user.customer_id
        token = request.POST.get('stripeToken')
        #create Stripe Card
        stripe_card_response=stripe.Customer.create_source(
           customer_id,
            source=token,
        )
        # save Stripe Card
        new_card_obj=Card.objects.get_or_create(
            billing_profile=billing_profile,
            stripe_id=stripe_card_response.id,
            brand=stripe_card_response.brand,
            country=stripe_card_response.country,
            exp_month=stripe_card_response.exp_month,
            exp_year=stripe_card_response.exp_year,
            last4=stripe_card_response.last4,
            )

        cart_obj, cart_created = Cart.objects.new_or_get(request)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        print("total:",order_obj.cart.total)
        card_obj=None
        # if card_obj is None:
        #     # cards=billing_profile.card_set.filter(default=True)
        #     if cards.exists():
        #         card_obj=cards.first()
        # if cards is None:
        #     return False,"No card Available"

        C_charge=stripe.Charge.create(
            amount=int(order_obj.cart.total*100),
            currency="usd",
            customer=customer_id,
            description="My First Test Charge (created for API docs)",

        )


        new_charge_obj=Charge.objects.get_or_create(
            billing_profile=billing_profile,
            stripe_id=C_charge.id,
            paid=C_charge.paid,
            refunded=C_charge.refunded,
            outcome=C_charge.outcome,

            seller_message=C_charge.outcome.get('seller_message'),
            risk_level=C_charge.outcome.get('risk_level')
            )
        print(new_charge_obj,"--")
    return redirect(reverse('carts:checkout'))


def successMsg(request):

    return render(request, 'my_success.html')

