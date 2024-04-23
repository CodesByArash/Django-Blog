from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, )
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .permissions import *
from .serializers import *
from .models import *
from blog.models import Article


# Create your views here.
class CommentDetailView(RetrieveUpdateDestroyAPIView, ):
    serializer_class   = CommentSerializer
    lookup_field       = "id"
    permission_classes = [CommentPermissionClass,]
    def get_queryset(self):
        slug  = self.kwargs.get('slug')
        article  = get_object_or_404(Article, slug = slug)

        return Comment.objects.filter(article=article)
    
class ArticleCommentsListView(ListCreateAPIView):
    serializer_class   = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    def get_queryset(self):
        slug  = self.kwargs.get('slug')
        article  = get_object_or_404(Article, slug = slug)

        return Comment.objects.filter(article=article)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['slug'] = self.kwargs.get('slug')
        return context


