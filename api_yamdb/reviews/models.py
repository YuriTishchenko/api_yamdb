from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from reviews.constants import NUMBER_OF_CHARS
from reviews.validators import validate_year


class User(AbstractUser):
    """Модель класса User унаследованная от AbstractUser"""

    class Role(models.TextChoices):
        USER = 'user', _('Пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')
        SUPERUSER = 'superuser', _('Суперюзер')

    username = models.CharField(
        max_length=150,
        verbose_name='Имя',
        unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+$')]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=40,
        verbose_name='Роль',
        choices=Role.choices,
        default=Role.USER,
    )

    class Meta:
        verbose_name = 'Позьзователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR


class Categorie(models.Model):
    """Модель для категорий."""
    name = models.CharField(
        verbose_name='название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для жанров."""
    name = models.CharField(
        verbose_name='название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для произведений."""
    name = models.CharField(
        verbose_name='название',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='год выпуска',
        validators=[
            validate_year
        ]
    )
    description = models.TextField(
        verbose_name='описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр',
    )
    category = models.ForeignKey(
        Categorie,
        verbose_name='категория',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов."""
    text = models.TextField('текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    score = models.SmallIntegerField(
        'оценка',
        validators=[
            MinValueValidator(1, message='Оценка должна быть не меньше 1'),
            MaxValueValidator(10, message='Оценка должна быть не больше 10')
        ]
    )
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[NUMBER_OF_CHARS]


class Comment(models.Model):
    """Модель комментариев."""
    reviews = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='комментируемый отзыв'
    )
    text = models.TextField('текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[NUMBER_OF_CHARS]
