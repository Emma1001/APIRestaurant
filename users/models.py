from django.contrib.auth.models import AbstractUser
from django.db import models

from users.choices import roles


class User(AbstractUser):

    role = models.CharField(max_length=10, choices=roles, blank=False, null=False)
    image = models.FileField(null=True, blank=True, upload_to='images')