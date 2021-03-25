from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from products.models import Product


class ProductModelSerializer(ModelSerializer):
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    price = MoneyField(max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = '__all__'

