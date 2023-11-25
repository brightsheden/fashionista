# forms.py

from django import forms
from .models import Blog, Product, ProductImage
from django.forms import inlineformset_factory
from ckeditor.widgets import CKEditorWidget

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
        widgets = {
            'content': CKEditorWidget(),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'thumbnail', 'images']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=3, max_num=3, can_delete=False)
