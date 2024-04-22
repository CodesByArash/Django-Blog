from rest_framework import serializers
from blog.models import Article, Category
from django.shortcuts import get_object_or_404
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model            = Category
        fields           = '__all__'
        read_only_fields = ["id",]


class ArticleSerializer(serializers.ModelSerializer):
    category_names = serializers.ListField(write_only=True, required=True)
    class Meta:
        model            = Article
        fields           = '__all__'
        read_only_fields = ["id", "status", "author"]
    
    def create(self, validated_data):
        category_names = validated_data.pop('category_names', [])
        categories = []
        for name in category_names:
            category = get_object_or_404(Category, name=name)
            categories.append(category)
            
        validated_data['author'] = self.context['request'].user
        article = super().create(validated_data)
        article.categories.set(categories)

        # article.author = self.context['request'].user
        article.save()

        return article

class ArticleStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Article
        fields           = '__all__'
        read_only_fields = ["id", "title", "slug", "author", "content", "publish",'created',  'updated' , 'categories']
