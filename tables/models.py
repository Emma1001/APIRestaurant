from django.db import models

from users.models import User


class Table(models.Model):
    number = models.PositiveIntegerField(unique=True, blank=False, null=False)
    capacity = models.PositiveIntegerField(blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tables')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='updated_tables')
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
