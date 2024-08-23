from rest_framework import serializers
from blog.models import Article, Category
from django.shortcuts import get_object_or_404

from .models import Category, Article, Rating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model            = Category
        fields           = '__all__'
        read_only_fields = ["id",]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'score', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    category_names = serializers.ListField(write_only=True, required=True)
    ratings = RatingSerializer(many=True, read_only=True)
    average_score = serializers.SerializerMethodField()
    user_score = serializers.SerializerMethodField()

    class Meta:
        model            = Article
        fields           = '__all__'
        read_only_fields = ["id", "status", "author",'ratings', 'average_score', 'user_score']
    
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
    
        def get_average_score(self, obj):
            ratings = obj.ratings.all()
            if ratings.exists():
                total_weight = sum(1 / (timezone.now() - rating.created_at).days for rating in ratings)
                weighted_sum = sum(rating.score / (timezone.now() - rating.created_at).days for rating in ratings)
                return weighted_sum / total_weight
            return 0

        def get_user_score(self, obj):
            user = self.context['request'].user
            rating = obj.ratings.filter(user=user).first()
            return rating.score if rating else None
        

class ArticleStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Article
        fields           = '__all__'
        read_only_fields = ["id", "title", "slug", "author", "content", "publish",'created',  'updated' , 'categories']
