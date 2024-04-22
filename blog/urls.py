from .views import *
from django.contrib import admin
from django.urls import path,include


app_name = "blog"

urlpatterns = [
    path("articles/",ArticleListView.as_view(), name="articles"),
    path("articles/<slug:slug>/", ArticleDetailView.as_view(), name="article-detail"),
    path("category/", CategoryListView.as_view(), name='categories'),
    path("category/<str:name>/",CategoryDetailView.as_view(), name="category-detail"),
    path("category/<str:name>/articles/", CategoryArticleListView.as_view(), name="category-articles"),
]