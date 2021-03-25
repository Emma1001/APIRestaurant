from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from categories.views import CategoryModelViewSet
from orders.views import OrderModelViewSet
from products.views import ProductModelViewSet
from tables.views import TableModelViewSet
from users.views import UserModelViewSet

router = routers.SimpleRouter()
router.register(r'categories', CategoryModelViewSet, basename='categories')
router.register(r'products', ProductModelViewSet, basename='products')
router.register(r'tables', TableModelViewSet, basename='tables')
router.register(r'orders', OrderModelViewSet, basename='orders')
router.register(r'users', UserModelViewSet, basename='users')

urlpatterns = [
                  path('admin/', admin.site.urls),

                  path('api-auth/', include('rest_framework.urls')),
                  path('orders/table/<int:table_id>/',
                       OrderModelViewSet.as_view({"get": "get_active_order_by_table_id"})),
                  path('', include('auth0authorization.urls'))
              ] + router.urls
