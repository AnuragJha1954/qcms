from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ("owner", "Store Owner"),
        ("staff", "Staff"),
    ]

    phone = models.CharField(max_length=15, blank=True, null=True)
    store_name = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="owner")

    def __str__(self):
        return self.username