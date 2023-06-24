from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator

from reviews.models import Categorie, Genre, Title
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from reviews.models import Categorie, Genre, Review, Title, User
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer,
    TokenSerializer,
    SignUpSerializer
)
from api.permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsUserOrModeratorOrReadOnly,
)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет Юзера"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для SignUp"""

    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        user, _ = User.objects.get_or_create(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='регистрация в api_yandb',
            message=f'confirmation_code: {confirmation_code}'
                    f' for {user.username}',
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для токенов"""

    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Неверный confirmation_code'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsUserOrModeratorOrReadOnly,)

    def get_queryset(self):
        return self.get_title().reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.get_review().comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, reviews=self.get_review())

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))
