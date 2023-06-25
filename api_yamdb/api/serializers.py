from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review
from reviews.models import Categorie, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorie
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categorie.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        if (
            self.context['request'].method == 'PUT'
            or self.context['request'].method == 'PATCH'
        ):
            return data
        elif Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs['title_id']
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор Юзера"""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

        def validate_username(self, username):
            if username == 'me':
                raise serializers.ValidationError(
                    'Имя me зарезервировано системой'
                )
            return username


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для создания учетки"""

    class Meta:
        model = User
        fields = ('username', 'email')

        def validate(self, data):
            if data.get('username') == 'me':
                raise serializers.ValidationError(
                    'Имя me зарезервировано системой'
                )


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для токена"""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\z',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )