from rest_framework import serializers
from blog.models import Article
from django.contrib.auth.models import User


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Article
        fields           = '__all__'
        read_only_fields = ["id","status"]

class ArticleStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Article
        fields           = '__all__'
        read_only_fields = ["id", "title", "slug", "author", "content", "publish",'created',  'updated' , 'categories']

