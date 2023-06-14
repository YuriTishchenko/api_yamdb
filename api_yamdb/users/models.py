from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        verbose_name='Biography',
        blank=True,
    )
    role = models.CharField(
        max_length=40,
        verbose_name='Role',
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
