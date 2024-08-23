from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Article, Rating
from .serializers import ArticleSerializer, RatingSerializer


from .models import Article
from .serializers import ArticleSerializer

from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404

from comment.permissions import IsAuthenticatedOrReadOnly
from .permissions import *
from .serializers import *
from .models import *
from .paginations import *
 
class ArticleListView(ListCreateAPIView):
    serializer_class   = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    pagination_class   = ArticleLimitOffsetPagination
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Article.objects.all()
            return Article.objects.filter(Q(status=True) | Q(author=user))

        return Article.objects.filter(status=True)

  
class ArticleDetailView(RetrieveUpdateDestroyAPIView, ):
    serializer_class   = ArticleSerializer
    lookup_field       = "slug"
    permission_classes = [IsAuthorOrStaffOrStatusTrue, ]
    def get_queryset(self):
        return Article.objects.all()
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ArticleStaffSerializer
        else:
            return ArticleSerializer
    
class CategoryListView(ListCreateAPIView):
    serializer_class   = CategorySerializer
    lookup_field       = "name"
    queryset           = Category.objects.all()
    permission_classes = [IsStaffOrReadOnly, ]
    pagination_class   = categoryLimitOffsetPagination

class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class   = CategorySerializer
    lookup_field       = "name"
    queryset           = Category.objects.all()
    permission_classes = [IsStaffOrReadOnly, ]

class CategoryArticleListView(ListAPIView):
    serializer_class   = ArticleSerializer
    pagination_class   = ArticleLimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        cat  = self.kwargs.get('name')
        cat  = get_object_or_404(Category, name = cat)
        if user.is_authenticated:
            if user.is_staff:
                return cat.articles.all()
            return cat.articles.filter((Q(status=True) | Q(author=user)))

        return cat.articles.filter(status=True)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated,]
        else:
            permission_classes = [AllowAny,]
        
        return [permission() for permission in permission_classes]
    
class ArticleSearchView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [SearchFilter]
    pagination_class = ArticleLimitOffsetPagination
    search_fields = ['content', 'title', "publish"]
    
    
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        article_id = request.data.get('article')
        score = request.data.get('score')

        rating, created = Rating.objects.update_or_create(
            user=user,
            article_id=article_id,
            defaults={'score': score, 'created_at': timezone.now()}
        )

        return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)
  