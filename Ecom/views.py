from django.shortcuts import render,get_object_or_404,Http404
from core.models import UserComment
from core.forms import UserCommentForm

# Create your views here.
def index(request):
    form=UserCommentForm(request.POST )
    if request.method=='POST':
        if form.is_valid():
            form.save()
            # return http.HttpResponseRedirect('')
    else:
        form = UserCommentForm()
    context={"form":form}
    return render(request,'index.html',context)