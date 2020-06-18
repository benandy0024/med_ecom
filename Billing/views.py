from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
from django.utils.http import is_safe_url
from accounts.forms import LoginForm,RegisterForm,GuestForm
from accounts.models import GuestEmail
from .models import BillingProfile
import stripe

# Create your views here.
def guest_register_page(request):
	form=GuestForm(request.POST or None)
	context = {
		'form': form,
	}
	next_=request.GET.get('next')
	next_post=request.POST.get('next')
	redirect_path=next_ or next_post or None
	if form.is_valid():
		email=form.cleaned_data.get("email")
		new_guest_email=GuestEmail.objects.create(email=email)
		request.session['guest_email_id']=new_guest_email.id
		if is_safe_url(redirect_path,request.get_host()):
			return redirect(redirect_path)
	return redirect('accounts:register')

STRIPE_PUB_KEY='pk_test_QZinzyFakYCKsVwpJI0ttgBC00VIepUNf2'
stripe.api_key="sk_test_HBJfc8IKGbe6DDjcIA2Jl8P900NGSbqtBI"
# def payment_method_view(request):
# 	if request.method == 'POST':
# 		print('Data:', request.POST)
#
# 	return render(request,'my_payment/payment-method.html',{"published_key":STRIPE_PUB_KEY})
#
#
#
#
# def payment_method_create_view(request):
# 	if request.method == 'POST':
# 		print('Data:', request.POST)
# 		stripe.Customer.create(
# 			email=request.POST['email'],
# 			nickname=request.POST['nickname']
# 		)
#
# 	return redirect(reverse('payment:success', args=[5]))



# def successMsg(request):
#
# 	return render(request, 'success.html',)






def payment_method_view(request):
	# if request.user.is_authenticated:
	# 	billing_profile=request.user.billingprofile
	# 	my_customer_id=billing_profile.customer_id
	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

	if not billing_profile:
		 print('ok')
	next_url = None
	next_ = request.GET.get('next')
	if is_safe_url(next_, request.get_host()):
		next_url=next_

	return render(request, 'index.html',{"next_url":next_url})


def charge(request):
    if request.method=="POST":
        print("DATA:",request.POST)
        # email=request.POST['email']
        # name=request.POST['nickname']
        # new_user = Customer.objects.create(name=name, email=email)
        # token = request.POST.get('stripeToken')
        # print(new_user)
        # customer = stripe.Customer.create(
        #     email=request.POST['email'],
        #     name=request.POST['nickname'],
        #     # source=token,
        # )
        # print(customer)
        # card = stripe.Customer.create_source(
        #     customer.id,
        #     source=token,
        # )
        # print(card)
        # stripe.Charge.create(
        # 	customer=customer,
        # 	amount=2000,
        # 	currency="usd",
        #
        # 	description="My First Test Charge (created for API docs)",
        # )
    return redirect(reverse('Payments:success'))


def successMsg(request):

	return render(request, 'my_success.html')

