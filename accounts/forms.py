from django import forms
# from django.contrib.auth import get_user_model
# User=get_user_model()
from core.models import User
class GuestForm(forms.Form):
    email = forms.CharField()


class LoginForm(forms.Form):
    username=forms.CharField(label='Your Pharmacy Name')
    password=forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    first_name = forms.CharField()
    last_name=forms.CharField()
    email=forms.EmailField()
    pharmacy_name = forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='confirm password',widget=forms.PasswordInput)

    def clean_username(self):
       username = self.cleaned_data.get("username")
       qs=User.objects.filter(username=username)
       if qs.exists():
            raise forms.ValidationError("username is taken")
       return username

    def clean_email(self):
       email = self.cleaned_data.get("email")
       qs=User.objects.filter(username=email)
       if qs.exists():
            raise forms.ValidationError("email is taken")
       return email

    def clean(self):
        data=self.cleaned_data
        password=self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        if password!=password2:
            raise forms.ValidationError("passwords must match!")
        return data



class UserDetailChangeForm(forms.ModelForm):
    username=forms.CharField(label='pharmacy_Name',required=False)
    class Meta:
        model=User
        fields=['first_name','last_name','username']