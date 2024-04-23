from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Comment
from blog.models import Article

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model     = Comment
        fields    = "__all__"
        read_only_fields = ["author", "id", "article", ]
    
    def create(self, validated_data):
        slug = self.context.get('slug')
        article      = get_object_or_404(Article, slug = slug)
        validated_data['article'] = article
        validated_data['author']  = self.context['request'].user
        article = super().create(validated_data)
        article.save()

        return article

