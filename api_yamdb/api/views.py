from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer)
from django.shortcuts import get_object_or_404, render
from rest_framework import filters, viewsets
from reviews.models import Categorie, Genre, Review, Title

from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    pass


def signup():
    pass


def token():
    pass


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
