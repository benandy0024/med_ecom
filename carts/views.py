from django.shortcuts import render,redirect
from.models import Product,Cart,CartItem
from Orders.models import Order
from accounts.forms import LoginForm,GuestForm
from Billing.models import BillingProfile
from accounts.models import GuestEmail
from Payments.views import charge

# Create your views here.
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products=cart_obj.cartitem_set.all()
    total=0
    for x in products:
        line_total = float(x.products.price) * x.quantity
        total += line_total
    print(total)
    print(cart_obj.total)
    cart_obj.total=total
    cart_obj.save()

    return render(request,'cart_home.html',{'cart':cart_obj})
def cart_update(request,slug):
    try:
        qty=request.GET.get('qty')
        update_qty = True
    except:
        qty=None
        update_qty=False
    try:
        product_obj=Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        print('product out of stock')
        return redirect('carts:cart_view')
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart_obj,products=product_obj )
    if created:
            print('created')
    if  update_qty and qty :
        if int(qty)==0 :
            cart_item.delete()
        else:
            cart_item.quantity=qty
            cart_item.save()
    else:
        pass
        # if product_obj in cart_obj.items.all():
        #     cart_obj.items.remove(cart_item)
        # else:
        #     cart_obj.items.add(cart_item)
    products = cart_obj.cartitem_set.all()
    request.session['cart_items'] = cart_obj.cartitem_set.count()


    return redirect('carts:cart_view')

def checkout_home(request):
    cart_obj,cart_created=Cart.objects.new_or_get(request)
    order_obj=None
    has_card=False
    if  cart_created or cart_obj.cartitem_set.count()==0:
        redirect('carts:cart_view')
    login_form=LoginForm()
    guest_form=GuestForm()
    # billing model manager
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        # order model manager
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        has_card=billing_profile.has_card
        # finalize checkout
    if request.method == "POST":
        "check the order is done"
        is_done = order_obj.check_done()

        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']


        return redirect('carts:success')
    context={
        'billing_profile':billing_profile,
        'object': order_obj,
        'login_form':login_form,
        'guest_form':guest_form,
        "has_card":has_card
    }
    return render(request,'checkout.html',context)

def checkout_done_view(request):
    return render(request,"checkout_done.html")