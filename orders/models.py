
from datetime import timedelta

from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField

from products.models import Product
from tables.models import Table
from users.models import User


class Order(models.Model):
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'

    StatusChoices = [
        (IN_PROGRESS, 'in_progress'),
        (COMPLETED, 'completed'),
    ]

    table = models.ForeignKey(Table, on_delete=models.PROTECT, blank=False, null=False, related_name='orders')
    status = models.CharField(max_length=12, choices=StatusChoices, default=IN_PROGRESS)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    products = models.ManyToManyField(Product, through='OrderProduct')


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False)
    product_price = MoneyField(decimal_places=2, max_digits=8, blank=False)
    product_quantity = models.PositiveIntegerField(blank=False)
