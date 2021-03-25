from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from orders.models import Order, OrderProduct
from products.models import Product


class OrderProductSerializer(ModelSerializer):
    product_price = MoneyField(max_digits=10, decimal_places=2)
    product_name = serializers.CharField(source='product.name')
    product_quantity = serializers.IntegerField()

    class Meta:
        model = OrderProduct
        fields = ('product_name', 'product_price', 'product_quantity')


class OrderModelSerializer(ModelSerializer):
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    table = serializers.StringRelatedField(many=False)
    user = serializers.StringRelatedField(many=False)
    products = OrderProductSerializer(source='orderproduct_set', many=True)

    class Meta:
        model = Order
        fields = '__all__'
        depth = 1
