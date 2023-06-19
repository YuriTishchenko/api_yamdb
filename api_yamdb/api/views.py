from django.shortcuts import render
from rest_framework import viewsets
from .mixins import ListCreateDestroyViewSet
from reviews.models import Categorie
from .serializers import CategorySerializer

class UserViewSet(viewsets.ModelViewSet):
    pass

class CommentViewSet(viewsets.ModelViewSet):
    pass

class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorySerializer
   # permission_classes
