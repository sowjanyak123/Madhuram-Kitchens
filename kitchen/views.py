from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm, MenuItemForm, OrderForm
from .models import Category, MenuItem, Order, OrderItem
from rest_framework import viewsets
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer, OrderItemSerializer

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
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.category = category
            menu_item.save()
            if 'add_another' in request.POST:
                return redirect('add_menu_item', category_id=category_id)
            elif 'add' in request.POST:
                return redirect('add_category')
            else:
                return redirect('menu_items')
    else:
        form = MenuItemForm()
    return render(request, 'add_menu_item.html', {'form': form, 'category': category})

def menu_items(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu_items.html', {'menu_items': menu_items})

def place_order(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('menu_items')
        items = MenuItem.objects.filter(id__in=selected_items)
        total_price = sum(item.price for item in items)
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = total_price
            order.save()
            for item in items:
                OrderItem.objects.create(order=order, menu_item=item, quantity=1)
            return redirect('order_confirmation', order_id=order.id)
        else:
            return render(request, 'place_order.html', {'form': form, 'menu_items': items, 'total_price': total_price})
    else:
        menu_items = MenuItem.objects.all()
        form = OrderForm()
        return render(request, 'place_order.html', {'form': form, 'menu_items': menu_items})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})


# API Views
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
