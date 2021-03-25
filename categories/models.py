from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    description = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, blank=True, on_delete=models.SET_NULL, null=True,
                                   related_name='updated_categories')
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    sub_category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True,
                                     related_name='sub_categories')

    def __str__(self):
        return '%s' % self.name
