from .views import *
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RatingViewSet


app_name = "blog"

router = DefaultRouter()
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path("articles/",ArticleListView.as_view(), name="articles"),
    path("articles/<slug:slug>/", ArticleDetailView.as_view(), name="article-detail"),
    path("category/", CategoryListView.as_view(), name='categories'),
    path("category/<str:name>/",CategoryDetailView.as_view(), name="category-detail"),
    path("category/<str:name>/articles/", CategoryArticleListView.as_view(), name="category-articles"),
    path("search/", ArticleSearchView.as_view(), name="search"),
    path('', include(router.urls)),
]