from django import forms
from products.models import Product,Category
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['title','description','price','category','image']
class ProductCategoryForm(forms.ModelForm):
    title=forms.CharField(label="Product Category",required=False)
    class Meta:
        model=Category
        fields=['title',]