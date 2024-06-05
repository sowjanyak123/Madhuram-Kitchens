from django.shortcuts import render, redirect
from .forms import CategoryForm, MenuItemForm
from .models import Category, MenuItem
from rest_framework import viewsets
from .serializers import CategorySerializer, MenuItemSerializer

# Form Views
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            if 'add_another_category' in request.POST:
                return redirect('add_category')
            else:
                return redirect('add_menu_item', category_id=category.id)
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

def add_menu_item(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.category = category  # Link menu item to the correct category
            menu_item.save()
            if 'add_another' in request.POST:
                return redirect('add_menu_item', category_id=category_id)
            elif 'add' in request.POST:
                return redirect('add_category')
            else:
                return redirect('results')
    else:
        form = MenuItemForm(initial={'category': category})
    return render(request, 'add_menu_item.html', {'form': form, 'category': category})

def results(request):
    menu_items = MenuItem.objects.select_related('category').all()
    return render(request, 'result.html', {'menu_items': menu_items})

# API Views
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
