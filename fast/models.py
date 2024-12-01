from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Supervisor', 'Supervisor'),
        ('Analyst', 'Analyst'),
        ('Viewer', 'Viewer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Analyst')
    is_blocked = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Custom related name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",  # Custom related name
        blank=True,
    )
