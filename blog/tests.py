from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.urls import reverse

from blog.models import Category, Article
from account.models import User
from comment.models import Comment
from .views import *


class ArticleListViewTestCase(APITestCase):
    def setUp(self):
        self.user     = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.save()
        self.category = Category(name="test", description="test")
        self.category.save()
        self.article  = Article(title="test", slug="test", author=self.user, content="test")
        self.article.categories.add(self.category)
        self.article.save()
        self.url      = reverse('blog:articles')

    def test_articles_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_articles_post(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.url,data={"title":"test1","category_names":["test"],"slug":"test1","content":"test updated"},format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ArticleDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user     = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.save()
        self.category = Category(name="test", description="test")
        self.category.save()
        self.article  = Article(title="test", slug="test", author=self.user, content="test")
        self.article.categories.add(self.category)
        self.article.status=True
        self.article.save()

        self.url      = reverse('blog:article-detail',kwargs={'slug':'test'})

    def test_article_detail_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_article_detail_put(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.put(self.url,data={"title":"test1","category_names":["test"],"slug":"test1","content":"test updated"},format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_article_detail_delete(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CategoryListViewTestCase(APITestCase):
    def setUp(self):
        self.user     = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.is_staff = True
        self.user.save()
        self.category = Category(name="test", description="test")
        self.category.save()
        self.url      = reverse('blog:categories')

    def test_categories_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_categories_post(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.url,data={"name":"test1","description":"test1"},format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CategoryDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user     = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.is_staff = True
        self.user.save()
        self.category = Category(name="test", description="test")
        self.category.save()
        self.article  = Article(title="test", slug="test", author=self.user, content="test")
        self.article.categories.add(self.category)
        self.article.status=True
        self.article.save()

        self.url      = reverse('blog:category-detail',kwargs={"name":'test'})

    def test_category_detail_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_category_detail_put_ok(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.put(self.url,data={"name":"test1","description":"test1"},format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_detail_delete_ok(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_category_detail_put_403(self):
        self.user.is_staff = False
        self.user.save()
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.put(self.url,data={"name":"test1"},format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_detail_delete_403(self):
        self.user.is_staff = False
        self.user.save()
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CategoryArticleListViewTestCase(APITestCase):
    def setUp(self):
        self.user     = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.save()
        self.category = Category(name="test", description="test")
        self.category.save()
        self.article  = Article(title="test", slug="test", author=self.user, content="test")
        self.article.categories.add(self.category)
        self.article.status=True
        self.article.save()
        self.url      = reverse('blog:category-articles',kwargs={"name":'test'})

    def test_category_articles_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class SearchListViewTestCase(APITestCase):
    def setUp(self):
        self.user     = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.save()
        self.category = Category(name="test", description="test")
        self.category.save()
        self.article  = Article(title="test", slug="test", author=self.user, content="test")
        self.article.categories.add(self.category)
        self.article.status=True
        self.article.save()
        self.url      = reverse('blog:search')+"?search=test"

    def test_category_articles_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    