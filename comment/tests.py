from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.urls import reverse

from blog.models import Category, Article
from account.models import User
from comment.models import Comment
from .views import CommentDetailView,ArticleCommentsListView

# Create your tests here.
class ArticleCommentsListViewTestCase(APITestCase):
    def setUp(self):
        self.user     = User(username="test", email="test@test.com", password="test")
        self.user.save()
        self.category = Category(name="test", description="test")
        self.category.save()
        self.article  = Article(title="test", slug="test", author=self.user, content="test")
        self.article.categories.add(self.category)
        self.article.save()
        self.comment  = Comment(article=self.article, author=self.user, content="test")
        self.comment.save()
        self.url      = reverse('comment:article-comments',kwargs={'slug':'test'})
        
    def test_comment_list_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_comment_post_ok(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.url,data={"content":"test"},format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CommentsDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user     = User(username="test", email="test@test.com", password="test")
        self.user.save()
        self.category = Category(name="test", description="test")
        self.category.save()
        self.article  = Article(title="test", slug="test", author=self.user, content="test")
        self.article.categories.add(self.category)
        self.article.save()
        self.comment  = Comment(article=self.article, author=self.user, content="test")
        self.comment.save()
        self.url      = reverse('comment:article-comment-detail',kwargs={'slug':'test','id':self.comment.id})

    def test_comment_detail_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_comment_detail_put(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.put(self.url,data={"content":"test updated"},format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_detail_delete(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
