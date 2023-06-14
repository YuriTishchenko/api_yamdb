from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель класса User унаследованная от AbstractUser"""
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=40,
        verbose_name='Роль',
    )

    class Meta:
        verbose_name = 'Позьзователь'
        verbose_name_plural = 'Пользователи'
