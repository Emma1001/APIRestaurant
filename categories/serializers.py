from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from categories.models import Category


class CategoryModelSerializer(ModelSerializer):
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    sub_categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = '__all__'

    # Get all Information for sub_categories
    # def get_fields(self):
    #     fields = super(CategoryModelSerializer, self).get_fields()
    #     fields['sub_categories'] = CategoryModelSerializer(many=True)
    #     return fields


