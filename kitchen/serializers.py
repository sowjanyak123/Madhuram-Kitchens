# hotel/serializers.py
from rest_framework import serializers
from .models import Category, MenuItem,Order,OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image']

class MenuItemSerializer(serializers.ModelSerializer):
     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

     class Meta:
        model = MenuItem
        fields = ['id', 'title', 'description', 'price', 'category']
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer()  # This will include the menu item data in the order item serialization
    
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)  # This will include the related order items in the order serialization
    
    class Meta:
        model = Order
        fields = '__all__'
