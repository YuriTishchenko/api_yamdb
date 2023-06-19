from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Review, Titles
from api.serializers import CommentSerializer, ReviewSerializer


class UserViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    pass


def signup():
    pass


def token():
    pass
  
  
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.get_title().reviews
         
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_title(self):
        return get_object_or_404(Titles, id=self.kwargs.get('title_id'))


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.get_review().comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, reviews=self.get_review())

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))
