from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.urls import reverse

from blog.models import Category, Article
from account.models import User
from comment.models import Comment
from .views import *
from .tokens import account_activation_token
from django.contrib.auth.tokens  import PasswordResetTokenGenerator
from .utils import temp_url

class TokenObtainPairViewTestCase(APITestCase):
    def setUp(self):
        self.user     = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.save()
        self.url      = reverse('account:token_obtain_pair')
    
    def test_token_obtain_success(self):
        response = self.client.post(self.url, data={"username":"test", "password":"test"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_obtain_fail(self):
        response = self.client.post(self.url, data={"username":"wrong_username", "password":"wrong password"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TokenRefreshViewTestCase(APITestCase):
    def setUp(self):
        self.user     = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.save()
        self.url      = reverse('account:token_refresh')
    
    def test_token_refresh_success(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.url, data={"refresh":str(refresh)}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_refresh_fail(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.url, data={"refresh":'invalid_refresh_token'}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TokenRevokeViewTestCase(APITestCase):
    def setUp(self):
        self.user     = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.save()
        self.url      = reverse('account:token_revoke')
    
    def test_token_revoke_success(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(self.url, data={"refresh":str(refresh)}, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_token_refresh_fail(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(self.url, data={"refresh":'invalid_refresh_token'}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PasswordChangeViewTestCase(APITestCase):
    def setUp(self):
        self.user     = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.save()
        self.url      = reverse('account:change-password')
    
    def test_passwordchange_success(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.put(self.url, data={"old_password":"test","new_password":"test1","confirm_password":"test1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_refresh_fail(self):
        self.user.set_password('test')
        self.user.save()
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.put(self.url, data={"old_password":"test11","new_password":"test2","confirm_password":"test1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.url, data={"old_password":"test","new_password":"test2","confirm_password":"test1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserViewTestCase(APITestCase):
    def setUp(self):
        self.user   = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.save()
    
    def test_userviewset_list_get(self):
        self.url = reverse('account:users-list')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_userviewset_list_post_success(self):
        self.url = reverse('account:users-list')
        response = self.client.post(self.url, data={"username":"test1","email":"test1@gmail.com","password":"test1","confirm_password":"test1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['username'],'test1')
    
    def test_userviewset_list_post_fail(self):
        self.url = reverse('account:users-list')
        response = self.client.post(self.url, data={"username":"test1112","email":"test1@gmail.com","password":"test_passwords_not_match","confirm_password":"test_password"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.url, data={"username":"test","email":"test_username_exits@gmail.com","password":"test","confirm_password":"test"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.url, data={"username":"test_email_exits","email":"test@test.com","password":"test","confirm_password":"test"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_userviewset_detail_get(self):
        self.url = reverse('account:users-detail',kwargs={"username":"test"})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_userviewset_detail_put(self):
        refresh      = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.url     = reverse('account:users-detail',kwargs={"username":"test"})
        response     = self.client.put(self.url,data={'username':'test_updated', 'password':'test_updated','email':'test_updated@test.com'},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_userviewset_detail_patch_success(self):
        refresh      = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.url     = reverse('account:users-detail',kwargs={"username":"test"})
        response     = self.client.patch(self.url,data={'username':'test_updated'},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_userviewset_detail_patch_fail(self):
        refresh      = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.user    = User(username="test1", email="test1@test.com")
        self.user.set_password('test1')
        self.user.save()
        self.url     = reverse('account:users-detail',kwargs={"username":"test1"})
        response     = self.client.patch(self.url,data={'username':'test_updated'},format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_userviewset_detail_delete_success(self):
        refresh      = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.url     = reverse('account:users-detail',kwargs={"username":"test"})
        response     = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_userviewset_detail_delete_fail(self):
        refresh      = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.user    = User(username="test1", email="test1@test.com")
        self.user.set_password('test1')
        self.user.save()
        self.url     = reverse('account:users-detail',kwargs={"username":"test1"})
        response     = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class EmailVerificationViewTestCase(APITestCase):
    def setUp(self):
        self.user  = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.save()
    
    def test_verify_email_get(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.url = reverse('account:verify-email')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
    
    def test_verify_email_post_success(self):
        token  = account_activation_token.make_token(self.user)
        uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        self.url = reverse('account:verify-email')+"?uidb64=" + uidb64 + "&token=" + token
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_verify_email_post_fail(self):
        token  = account_activation_token.make_token(self.user)
        self.url = reverse('account:verify-email')+"?uidb64=" + "wrong_uidb64" + "&token=" + "wrong_token"
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class RequestResetPasswordViewTestCase(APITestCase):
    def setUp(self):
        self.user  = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.save()
    
    def test_forget_password_post_success(self):
        self.url = reverse('account:request-reset-password')
        response = self.client.post(self.url, data = {"email":"test@test.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_forget_password_post_fail(self):
        self.url = reverse('account:request-reset-password')
        response = self.client.post(self.url, data = {"email":"test_does_not_exists@test.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ResetPassowordViewTestCase(APITestCase):
    def setUp(self):
        self.user  = User(username="test", email="test@test.com")
        self.user.set_password('test')
        self.user.save()
    
    def test_forget_password_post(self):
        token  = PasswordResetTokenGenerator().make_token(self.user)
        uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        self.url = reverse('account:reset-password')+"?uidb64=" + uidb64 + "&token=" + token
        response = self.client.post(self.url,data={"new_password":"test_password","confirm_password":"test_password"},format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
