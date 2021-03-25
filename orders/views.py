from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orders.models import Order, OrderProduct
from orders.serializers import OrderModelSerializer
from products.models import Product
from tables.models import Table
from users.models import User
from users.permissions import CreateOrder, DeleteOrder


class OrderModelViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated | ReadOnly]

    serializer_class = OrderModelSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['status', 'table', 'user']
    ordering_fields = ['status', 'table', 'user']

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'PATCH':
            permission_classes = [CreateOrder]
        if self.request.method == 'DELETE':
            permission_classes = [DeleteOrder]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Order.objects.filter(is_deleted=0)

    def create(self, request, *args, **kwargs):
        data = request.data

        table = Table.objects.get(number=data["table"])

        has_active_order = Order.objects.filter(status="IN_PROGRESS",
                                                table_id=getattr(table, "id"),
                                                is_deleted=0)

        if has_active_order.exists():
            return Response("There is already order on that table!",
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.first()

        new_order = Order.objects.create(table=table,
                                         status=data["status"],
                                         user=user,
                                         is_deleted=data["is_deleted"])

        new_order.save()

        for product in data["products"]:
            product_obj = Product.objects.get(name=product["product_name"])
            OrderProduct.objects.create(product_price_currency=getattr(product_obj, "price_currency"),
                                        product_price=getattr(product_obj, "price"),
                                        product_quantity=product["product_quantity"],
                                        order_id=getattr(new_order, "id"),
                                        product_id=getattr(product_obj, "id"))

        serializer = OrderModelSerializer(new_order)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        if getattr(instance, 'status').lower() == 'completed':
            return Response("Can't update completed order", status=status.HTTP_400_BAD_REQUEST)
        data = request.data

        table = Table.objects.get(number=data["table"])

        has_active_order = Order.objects.filter(status="IN_PROGRESS",
                                                table_id=getattr(table, "id"),
                                                is_deleted=0,
                                                ).exclude(id=getattr(instance, 'id'))

        if has_active_order.exists():
            return Response("There is already order on that table!",
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.first()

        instance.table = table
        instance.status = data["status"]
        instance.user = user
        instance.is_deleted = data["is_deleted"]

        instance.save()

        OrderProduct.objects.filter(order_id=getattr(instance, 'id')).delete()

        for product in data["products"]:
            product_obj = Product.objects.get(name=product["product_name"])
            OrderProduct.objects.create(product_price_currency=getattr(product_obj, "price_currency"),
                                        product_price=getattr(product_obj, "price"),
                                        product_quantity=product["product_quantity"],
                                        order_id=getattr(instance, "id"),
                                        product_id=getattr(product_obj, "id"))

        serializer = OrderModelSerializer(instance)

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs['pk'])

        order.is_deleted = 1
        order.save()

        return Response("Deleted successfully!", status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def get_active_order_by_table_id(self, request, *args, **kwargs):
        table_id = int(kwargs['table_id'])

        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            return Response("Table not found", status=status.HTTP_404_NOT_FOUND)

        order = table.orders.filter(is_deleted=0,
                                    status="IN_PROGRESS").first()
        if not order:
            return Response("There is no order for that table", status=status.HTTP_404_NOT_FOUND)

        serializer = OrderModelSerializer(order)

        return Response(serializer.data)
