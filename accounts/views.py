from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from core.models import  User
from .forms import RegisterForm,LoginForm,UserDetailChangeForm
from django.utils.http import is_safe_url
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from.signals import user_logged_in
from django.views.generic import DetailView,UpdateView
from django.utils.decorators import method_decorator
# Create your views here.
# @login_required()
# def accounts_home_view(request):
#     return render(request,'account/home.html')

#LoginRequiredMixin
class AccountHomeView(LoginRequiredMixin,DetailView):
    template_name = "account/home.html"
    def get_object(self):
        return self.request.user

def register_page(request):

    if request.method=="POST":
        print(request.method)
        pharmacy= request.POST["pharma"]
        first_name =request.POST["fname"]
        last_name = request.POST["lname"]
        email = request.POST["email"]
        password = request.POST["pass"]
        cpassword = request.POST["cpass"]

        if password==cpassword:
            if User.objects.filter(username=pharmacy).exists():
                messages.info(request,"Username taken")
                redirect('accounts:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"E-mail taken")
                redirect('accounts:register')
            else:

                new_user=User.objects.create_user(
                    username=pharmacy,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name)
                new_user.save()
                print(new_user,"created")
        else:
            messages.info(request, "Password not Matching..")
            redirect('accounts:register')
    context={

    }
    return render(request,'auth/register.html',context)


def login_page(request):
    form=LoginForm(request.POST or None)
    context={"form":form}
    next_=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path=next_ or next_post or None
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del  request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('products:list')
        else:
            # Return an 'invalid login' error message.
            messages.info(request, "Password not correct..")
    return render(request,'auth/login.html',context)

class UserUpdateView(LoginRequiredMixin,UpdateView):
    form_class=UserDetailChangeForm
    template_name = 'auth/update-form.html'

    def get_object(self):
        return self.request.user
    def get_context_data(self,*args, **kwargs):
        context=super(UserUpdateView, self).get_context_data(*args,**kwargs)
        context['title']='Change your Account Details'
        return context
    def get_success_url(self):
        return reverse('accounts:account')
