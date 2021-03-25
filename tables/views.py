from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from tables.models import Table
from tables.serializers import TableModelSerializer


class TableModelViewSet(ReadOnlyModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableModelSerializer
