from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.shortcuts import render
from django.db.models import Q

from .permissions import *
from .serializers import *
from .models import *


# Create your views here.

class ArticleList(ListCreateAPIView):
    serializer_class   = ArticleSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Article.objects.all()
            return Article.objects.filter(Q(status=True) | Q(author=user))

        return Article.objects.filter(status=True)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated,]
        else:
            permission_classes = [AllowAny,]
        
        return [permission() for permission in permission_classes]

    
    
class ArticleDetail(RetrieveUpdateDestroyAPIView, ):
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
    
    