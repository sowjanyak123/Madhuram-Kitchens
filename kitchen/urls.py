from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import add_category, add_menu_item, results, CategoryViewSet, MenuItemViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'menuitems', MenuItemViewSet)

urlpatterns = [
    path('', add_category, name='add_category'),
    path('add_menu_item/<int:category_id>/', add_menu_item, name='add_menu_item'),
    path('results/', results, name='results'),
    path('api/', include(router.urls)),
]
