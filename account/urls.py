from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', Register.as_view()),
    path('forget-password/', PasswordForget.as_view(), name='forget-password'),
    path('change-password/', PasswordChange.as_view(), name='change-password'),
    path('token/revoke/', TokenRevoke.as_view(), name='revoke-token'),
    path('verify-email/', EmailVerification.as_view(), name='verify-email'),
    
]