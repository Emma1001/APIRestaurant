from unittest.mock import patch

from django.test import TestCase
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APIRequestFactory, force_authenticate

from categories.models import Category
from orders.models import Order
from orders.views import OrderModelViewSet
from products.models import Product
from tables.models import Table
from users.models import User


class TestCaseOrders(TestCase):
    def setUp(self):
        self.table_one = Table.objects.create(number=1, capacity=2)
        self.table_two = Table.objects.create(number=2, capacity=4)
        self.table_three = Table.objects.create(number=3, capacity=4)
        category = Category.objects.create(name='Meat')
        product = Product.objects.create(name='Chicken', code=100, price=12.00, category=category)

        self.order = Order.objects.create(table=self.table_one, status='IN_PROGRESS')
        self.order_completed = Order.objects.create(table=self.table_one, status='COMPLETED')
        self.order_update_busy_table = Order.objects.create(table=self.table_three, status='IN_PROGRESS')

    def test_create_new_order(self):
        factory = APIRequestFactory()
        data = {
            'table': getattr(self.table_two, "number"),
            'status': 'IN_PROGRESS',
            'products': [
                {
                    "product_name": "Chicken",
                    "product_price": "12.90",
                    "product_quantity": 2
                }
            ],
            'is_deleted': False
        }
        request = factory.post('/orders', data=data, format='json')

        with patch('orders.views.OrderModelViewSet.get_permissions'):
            order_detail = OrderModelViewSet.as_view({'post': 'create'})
            response = order_detail(request)

            self.assertEqual(response.status_code, 200)

    def test_create_order_in_progress_on_busy_table(self):
        factory = APIRequestFactory()
        data = {
            'table': getattr(self.table_one, "number"),
            'status': 'IN_PROGRESS',
            'products': [
                {
                    "product_name": "Chicken",
                    "product_price": "12.90",
                    "product_quantity": 2
                }
            ],
            'is_deleted': False
        }
        request = factory.post('/orders', data=data, format='json')

        with patch('orders.views.OrderModelViewSet.get_permissions'):
            order_detail = OrderModelViewSet.as_view({'post': 'create'})
            response = order_detail(request)

            self.assertEqual(response.status_code, 400)

    def test_update_completed_order(self):
        factory = APIRequestFactory()
        data = {
            'table': getattr(self.table_one, "number"),
            'status': 'IN_PROGRESS',
            'products': [
                {
                    "product_name": "Chicken",
                    "product_price": "12.90",
                    "product_quantity": 2
                }
            ],
            'is_deleted': False
        }
        request = factory.put('/orders/%s/' % self.order_completed.pk, data=data, format='json')

        with patch('orders.views.OrderModelViewSet.get_permissions'):
            order_detail = OrderModelViewSet.as_view({'put': 'update'})
            response = order_detail(request, **{'pk': self.order_completed.pk})

            self.assertEqual(response.status_code, 400)

    def test_update_order_on_busy_table(self):
        factory = APIRequestFactory()
        data = {
            'table': getattr(self.table_one, "number"),
            'status': 'IN_PROGRESS',
            'products': [
                {
                    "product_name": "Chicken",
                    "product_price": "12.90",
                    "product_quantity": 2
                }
            ],
            'is_deleted': False
        }
        request = factory.put('/orders/%s/' % self.order_update_busy_table.pk, data=data, format='json')

        with patch('orders.views.OrderModelViewSet.get_permissions'):
            order_detail = OrderModelViewSet.as_view({'put': 'update'})
            response = order_detail(request, **{'pk': self.order_update_busy_table.pk})

            self.assertEqual(response.status_code, 400)