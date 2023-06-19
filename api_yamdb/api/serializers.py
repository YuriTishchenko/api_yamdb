from rest_framework import serializers

from reviews.models import Categories, Comments, Genres, Reviews, Titles, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }