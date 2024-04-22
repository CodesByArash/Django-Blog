from .views import *
from django.contrib import admin
from django.urls import path,include


app_name = "blog"

urlpatterns = [
    path("articles/",ArticleListView.as_view(), name="articles"),
    path("articles/<slug:slug>/", ArticleDetailView.as_view(), name="article-detail"),
    path("articles/category/<str:name>/", CategoryArticleListView.as_view(), name="category-articles"),
    path("categories", CategoryListView.as_view(), name='categories'),
    path("categories/<str:name>/",CategoryDetailView.as_view(), name="category-detail")
]