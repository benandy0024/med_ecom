from django.shortcuts import render,get_object_or_404,Http404
from django.views.generic import ListView,DetailView
from .models import Product,Category
from carts.models import Cart,CartItem
from analytics.mixin import ObjectViewedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator,EmptyPage ,PageNotAnInteger
from django.contrib.contenttypes.models import ContentType
# Create your views here.
def home(request):
    qs=Product.objects.all()
    cat=Category.objects.all()
    for item in qs:
        print(item.category.all())
    context={
        'qs':qs,
        'cat':cat
    }
    return render(request,'medecine/home.html',context)
class ProductListView(ListView):
    template_name = 'medecine/list_view.html'
    paginate_by = 8
    def get_queryset(self, *args, **kwargs):
        request = self.request

        return Product.objects.all()

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs, )
        cat = Category.objects.all()
        context['cat'] = cat
        return context
        # search




class UserProductHistoryView(LoginRequiredMixin,ListView):
    template_name = 'medecine/user-history.html'
    def get_queryset(self, *args, **kwargs):
        request = self.request
        views=request.user.objectviewed_set.by_model(Product,model_queryset=False)
        # viewed_ids=[x.object_id for x in views]
        # Product.objects.filter(pk__in=viewed_ids)
        return views

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs, )
        cat = Category.objects.all()
        context['cat'] = cat
        return context
        # search








#ObjectViewedMixin
class ProductDetailView(ObjectViewedMixin,LoginRequiredMixin,DetailView):
    queryset =  Product.objects.all()
    template_name = 'medecine/detail_view.html'
    def get_context_data(self,*args, **kwargs,):
        context=super(ProductDetailView, self).get_context_data(*args, **kwargs,)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        cartitem=cart_obj.cartitem_set.all()
        context['carts']=cart_obj
        return context

    #raise Http404 error
    def get_object(self, queryset=None, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:

            raise Http404("Not Found")
        except Product.MultipleObjectsReturned:
            #  get_by_id(slug) model manager method
            qs = Product.objects.get_by_id(slug)
            instance = qs.first()
        except:
            raise Http404('hmmmm')

        return instance

# class MostViewedProduct(HitCountDetailView):
#     queryset =  Product.objects.all()
#     context_object_name = 'post'
#     template_name = 'medecine/list.html'
#     def get_context_data(self,*args, **kwargs,):
#         context=super(MostViewedProduct, self).get_context_data(*args, **kwargs,)
#         context.update({
#             'popular_posts': Product.objects.order_by('-hit_count_generic__hits')[:3],
#         })
#         return context
#
#     #raise Http404 error
#     def get_object(self, queryset=None, *args, **kwargs):
#         request = self.request
#         slug = self.kwargs.get('slug')
#         try:
#             instance = Product.objects.get(slug=slug)
#         except Product.DoesNotExist:
#
#             raise Http404("Not Found")
#         except Product.MultipleObjectsReturned:
#             #  get_by_id(slug) model manager method
#             qs = Product.objects.get_by_id(slug)
#             instance = qs.first()
#         except:
#             raise Http404('hmmmm')
#
#         return instance

def product_category(request,slug):
    #getting the 404 error
    instance = get_object_or_404(Category,slug=slug)

    context={
        'instance':instance

    }

    return render(request,'medecine/list.html',context)