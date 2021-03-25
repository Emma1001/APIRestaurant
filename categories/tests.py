from django.test import TestCase
from rest_framework.test import APIRequestFactory, CoreAPIClient, ForceAuthClientHandler, force_authenticate

from categories.models import Category
from categories.views import CategoryModelViewSet

from requests.auth import HTTPBasicAuth

from products.models import Product
from users.models import User


class TestCase(TestCase):
    def setUp(self):
        food_category = Category.objects.create(name='Food')
        food_assigned_product_category = Category.objects.create(name='FoodWithAssignedProduct')
        Category.objects.create(name='Meat', sub_category=food_category)
        Product.objects.create(name='Chicken', code=100, price=12.00, category=food_assigned_product_category)

    def test_initial_is_deleted(self):
        category = Category.objects.get(name='Food')

        self.assertEqual(category.is_deleted, False)

    def test_view_set_get(self):
        request = APIRequestFactory().get("")
        category_detail = CategoryModelViewSet.as_view({'get': 'retrieve'})
        category = Category.objects.get(name='Food')
        response = category_detail(request, pk=category.pk)
        self.assertEqual(response.status_code, 200)

    def test_view_set_destroy(self):
        factory = APIRequestFactory()
        category = Category.objects.get(name='Meat')
        request = factory.delete('/categories/%s/' % category.pk)
        force_authenticate(request, user=User.objects.create(username='s'))
        category_detail = CategoryModelViewSet.as_view({'delete': 'destroy'})
        response = category_detail(request, **{'pk': category.pk})

        self.assertEqual(response.status_code, 200)

    def test_view_set_destroy_with_sub_categories(self):
        factory = APIRequestFactory()
        category = Category.objects.get(name='Food')
        request = factory.delete('/categories/%s/' % category.pk)
        force_authenticate(request, user=User.objects.create(username='s'))
        category_detail = CategoryModelViewSet.as_view({'delete': 'destroy'})
        response = category_detail(request, **{'pk': category.pk})

        self.assertEqual(response.status_code, 400)

    def test_view_set_destroy_with_assigned_product(self):
        factory = APIRequestFactory()
        category = Category.objects.get(name='FoodWithAssignedProduct')
        request = factory.delete('/categories/%s/' % category.pk)
        force_authenticate(request, user=User.objects.create(username='s'))
        category_detail = CategoryModelViewSet.as_view({'delete': 'destroy'})
        response = category_detail(request, **{'pk': category.pk})

        self.assertEqual(response.status_code, 400)
