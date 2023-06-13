from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Titles(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genres
    )
    category = models.ForeignKey(
        Categories
    )


class Reviews(models.Model):
    pass


class Comments(models.Model):
    pass