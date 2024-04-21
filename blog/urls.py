from .views import *
from django.contrib import admin
from django.urls import path,include


app_name = "blog"

urlpatterns = [
    path("",ArticleList.as_view(), name="list"),
    path("<slug:slug>/",ArticleDetail.as_view(), name="detail"),

]