from django.db import models

from validators import validate_year


class Categories(models.Model):
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Genres(models.Model):
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Titles(models.Model):
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
        Genres,
        verbose_name='жанр',
    )
    category = models.ForeignKey(
        Categories,
        verbose_name='категория',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name
