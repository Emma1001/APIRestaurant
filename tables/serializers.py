from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from tables.models import Table


class TableModelSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Table
        fields = '__all__'
