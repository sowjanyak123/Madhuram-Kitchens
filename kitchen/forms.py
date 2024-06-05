from django import forms
from .models import Category, MenuItem

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']

class MenuItemForm(forms.ModelForm):
    category =forms.ModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = MenuItem
        fields = ['title', 'description', 'price', 'category']