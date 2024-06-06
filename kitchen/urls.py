from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, MenuItemViewSet, OrderViewSet, OrderItemViewSet,add_category,add_menu_item,menu_items,place_order,order_confirmation

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'menuitems', MenuItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'orderitems', OrderItemViewSet)

urlpatterns = [
    path('add_category/', add_category, name='add_category'),
    path('add_menu_item/<int:category_id>/', add_menu_item, name='add_menu_item'),
    path('menu_items/', menu_items, name='menu_items'),
    path('place_order/', place_order, name='place_order'),
    path('order_confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('api/', include(router.urls)),
]
