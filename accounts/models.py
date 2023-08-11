from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Add custom fields here, if needed

    # Provide unique related_name values to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Use a unique related_name
        blank=True,
        verbose_name="groups",
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_query_name="customuser",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Use a unique related_name
        blank=True,
        verbose_name="user permissions",
        help_text="Specific permissions for this user.",
        related_query_name="customuser",
    )

    def __str__(self):
        return self.username
