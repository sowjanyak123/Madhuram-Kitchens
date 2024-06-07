from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm, MenuItemForm, OrderForm
from .models import Category, MenuItem, Order, OrderItem
from django.contrib import messages
from django.http import HttpResponse
import datetime
from decimal import Decimal

# Form Views

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            if Category.objects.filter(name=category_name).exists():
                messages.error(request, 'Category already exists.')
            else:
                category = form.save()
                if 'add_another_category' in request.POST:
                    return redirect('add_category')
                else:
                    return redirect('add_menu_item', category_id=category.id)
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

def add_menu_item(request, category_id=None):
    if category_id:
        category = get_object_or_404(Category, id=category_id)
    else:
        category = None

    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if MenuItem.objects.filter(title=title, category=form.cleaned_data['category']).exists():
                messages.error(request, 'Menu item already exists in this category.')
            else:
                menu_item = form.save(commit=False)
                menu_item.category = form.cleaned_data['category']
                menu_item.save()
                if 'add_another' in request.POST:
                    return redirect('add_menu_item', category_id=menu_item.category.id)
                else:
                    return redirect('menu_items')
    else:
        form = MenuItemForm(initial={'category': category})
    return render(request, 'add_menu_item.html', {'form': form, 'category': category})


def menu_items(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()

    if request.method == 'POST':
        selected_items = request.POST.getlist('menu_items')
        quantities = request.POST.getlist('quantities')

        order_items = []
        total_price = Decimal('0.00')

        for item_id, quantity in zip(selected_items, quantities):
            item = MenuItem.objects.get(id=item_id)
            item_total_price = item.price * Decimal(quantity)
            total_price += item_total_price
            order_items.append({
                'menu_item_id': item.id,
                'menu_item_title': item.title,
                'quantity': quantity,
                'price': float(item_total_price)
            })

        request.session['order_items'] = order_items
        request.session['total_price'] = float(total_price)

        return redirect('place_order')

    return render(request, 'menu_items.html', {'menu_items': menu_items, 'categories': categories})

def place_order(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        phone_number = request.POST.get('phone_number')

        request.session['customer_name'] = customer_name
        request.session['phone_number'] = phone_number

        return redirect('order_review')

    return render(request, 'place_order.html')

def order_review(request):
    order_items = request.session.get('order_items')
    total_price = request.session.get('total_price')
    customer_name = request.session.get('customer_name')
    phone_number = request.session.get('phone_number')

    if not order_items or not customer_name or not phone_number:
        return redirect('menu_items')

    if request.method == 'POST':
        order = Order.objects.create(
            customer_name=customer_name,
            phone_number=phone_number,
            total_price=Decimal(total_price),
            created_at=datetime.datetime.now()
        )

        for item in order_items:
            menu_item = MenuItem.objects.get(id=item['menu_item_id'])
            OrderItem.objects.create(order=order, menu_item=menu_item, quantity=item['quantity'])

        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'order_review.html', {
        'order_items': order_items,
        'total_price': total_price,
        'customer_name': customer_name,
        'phone_number': phone_number
    })

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    total_price = sum(item.menu_item.price * item.quantity for item in order_items)
    return render(request, 'order_confirmation.html', {'order': order, 'order_items': order_items, 'total_price': total_price})


def dashboard(request):
    return render(request,'home.html')


# API Views
from rest_framework import viewsets
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer, OrderItemSerializer

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
