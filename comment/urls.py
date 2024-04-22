from .views import *
from django.contrib import admin
from django.urls import path,include

app_name = "comment"

urlpatterns = [
    path('articles/<slug:slug>/comments/', ArticleCommentsListView.as_view(), name="article-comments"),
    path('articles/<slug:slug>/comments/<str:id>/', CommentDetailView.as_view(), name="article-comment-detail"),
]