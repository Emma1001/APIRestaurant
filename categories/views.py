import json

import jwt
from rest_framework import status

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from categories.models import Category
from categories.serializers import CategoryModelSerializer


class CategoryModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategoryModelSerializer

    def get_queryset(self):
        return Category.objects.filter(is_deleted=0)

    def destroy(self, request, *args, **kwargs):
        category = Category.objects.get(id=self.kwargs['pk'])

        if category.products.all() or category.sub_categories.all():
            return Response("Can't delete category!",
                            status=status.HTTP_400_BAD_REQUEST)

        category.is_deleted = 1
        category.save()

        return Response("Deleted successfully!", status=status.HTTP_200_OK)

