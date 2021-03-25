from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from products.models import Product
from products.serializers import ProductModelSerializer
from users.permissions import AddMenuItems


class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductModelSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['category_id', 'name']
    ordering_fields = ['category', 'name']

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticatedOrReadOnly]
        if self.request.method == 'POST':
            permission_classes = [AddMenuItems]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Product.objects.filter(is_deleted=0)

    def destroy(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['pk'])
        product.is_deleted = 1
        product.save()

        return Response("Deleted successfully!", status=status.HTTP_200_OK)
