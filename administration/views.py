from django.shortcuts import render,redirect,get_object_or_404
from.forms import ProductForm,ProductCategoryForm
from django.views.generic import ListView,DetailView
from products.models import Product
from Orders.models import Order
from carts.models import CartItem
from django.core.paginator import Paginator,EmptyPage ,PageNotAnInteger
# Create your views here.
def home(request):
    return render(request,'administration/home.html')
def view_order(request):
    order_qs=Order.objects.all().order_by("-timestamp")
    cart_item_qs=CartItem.objects.all()
    # search
    query = request.GET.get('q')
    if query is not None:
        order_qs = order_qs.filter(order_id__icontains=query)
    #pagination
    paginator = Paginator(order_qs, 10)  # show items per page
    page = request.GET.get('page')
    try:
        order_qs = paginator.page(page)
    except PageNotAnInteger:
        order_qs = paginator.page(1)
    except EmptyPage:
        order_qs = paginator.page(paginator.num_pages)

    context={
        "order_qs":order_qs,
        "cart_item_qs":cart_item_qs
    }
    return render(request,'administration/view_order.html',context)

class ProductListView(ListView):
    template_name ='administration/list_product.html'
    paginate_by = 2
    def get_queryset(self):
        self.request
        return Product.objects.all()
def add_product(request):
    form=ProductForm(request.POST , request.FILES)
    cat_form=ProductCategoryForm(request.POST)
    if request.method=='POST':
        if form.is_valid() :
            form.save()
            return redirect('administration:list')
        elif cat_form.is_valid():
            cat_form.save()
            return redirect('administration:add')
    else:
        form=ProductForm()
        cat_form = ProductCategoryForm()
    context={
        "form":form,
        'cat_form':cat_form
    }
    return render(request,'administration/add-product.html',context)

def update(request,slug):
    product_form=Product.objects.get(slug=slug)
    form=ProductForm(instance=product_form)
    if request.method=='POST':
        form = ProductForm(request.POST, request.FILES,instance=product_form)
        if form.is_valid():
            form.save()

            return redirect('administration:list')
    context={
        "form":form,
    }
    return render(request,'administration/add-product.html',context)
def delete(request,slug):
    product_form = Product.objects.get(slug=slug)
    if request.method=="POST":
        product_form.delete()
        return redirect('administration:list')
    context={
        "product":product_form
    }
    return render(request,'administration/delete.html',context)

def order_detail(request,id):
    instance=get_object_or_404(Order,id=id)

    context={
        "instance":instance
    }
    return render(request, 'administration/order_detail.html', context)