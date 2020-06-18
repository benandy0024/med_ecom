from django import forms
from.models import UserComment
class UserCommentForm(forms.ModelForm):
    comment=forms.CharField(label="Comments/Queries",widget=forms.Textarea(attrs={'size': '40'}))
    class Meta:
        model=UserComment
        fields=["name","contact","pharmacy_name","email","comment"]