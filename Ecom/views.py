from django.shortcuts import render,get_object_or_404,Http404
from core.models import UserComment
from core.forms import UserCommentForm
from products.models import Category
# Create your views here.
def index(request):
    cat = Category.objects.all()
    form=UserCommentForm(request.POST )
    if request.method=='POST':
        if form.is_valid():
            form.save()
            # return http.HttpResponseRedirect('')
    else:
        form = UserCommentForm()
    context={"form":form,
             'cat': cat
             }
    return render(request,'index.html',context)