# forms.py

from django import forms
from .models import Category, MenuItem, Order

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['title', 'description', 'price', 'category',]

class OrderForm(forms.ModelForm):
    customer_name = forms.CharField(max_length=100)
    mobile_number = forms.CharField(max_length=15)

    class Meta:
        model = Order
        fields = ['customer_name', 'mobile_number']
