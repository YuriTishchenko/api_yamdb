from django.db.models import Q
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

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category')


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('__all__',)


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
        if self.context['request'].method != 'POST':
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


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для создания учетки"""

    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Имя me зарезервировано системой')
        check_email = User.objects.filter(email=data.get('email'))
        check_user = User.objects.filter(username=data.get('username'))
        test_pair_of_user_and_mail = User.objects.filter(
            Q(email=data.get('email')) & Q(username=data.get('username'))
        )
        if (check_email and not check_user):
            raise serializers.ValidationError(
                'Адрес электронной почты занят'
            )

        if check_user:
            if not test_pair_of_user_and_mail:
                raise serializers.ValidationError(
                    'Неверный адрес  электронной почты'
                )
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для токена"""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )
