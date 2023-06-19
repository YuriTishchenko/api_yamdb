from rest_framework import serializers

from reviews.models import Categories, Comments, Genres, Reviews, Titles, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        exclude = ('id',)
        lookup_field = 'name'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        exclude = ('id',)
        lookup_field = 'name'


class TitleSerializer(serializers.ModelSerializer):
    genere = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Titles
        fields = '__all__'

