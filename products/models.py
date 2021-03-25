from django.db import models

from categories.models import Category
from users.models import User

from djmoney.models.fields import MoneyField


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    code = models.PositiveIntegerField(unique=True, blank=False)
    description = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=False, null=False, related_name='products')
    price = MoneyField(decimal_places=2, max_digits=8, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='updated_products')
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
