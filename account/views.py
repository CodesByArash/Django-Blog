from rest_framework.response import Response
from rest_framework import viewsets
# from rest_framework.generics import (UpdateAPIView, RetrieveAPIView, ListAPIView,)
from rest_framework.views import APIView
from rest_framework.decorators import (api_view, permission_classes,)
from rest_framework.permissions import (IsAuthenticated, AllowAny,)
from rest_framework import status




from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.utils.encoding import (smart_str, smart_bytes, )
from django.utils.http import (urlsafe_base64_decode, urlsafe_base64_encode,)
from django.contrib.auth import login
from django.shortcuts import redirect


from .serializers import *
from .utils import *
from .models import *
from .tokens import account_activation_token
from .permissions import *

from django.contrib.auth import get_user_model
User = get_user_model()



class TokenRevokeView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        request.auth.delete()
        return Response(status=204)

class EmailVerificationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(request):
        user = request.user
        if user.is_email_verified:
            return Response({'message': 'your email is verified preveously'}, status=status.HTTP_400_BAD_REQUEST)
        
        ''' # token  = account_activation_token.make_token(user) 
        # uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

        # current_site = get_current_site(request=request).domain
        # relativeLink = reverse('EmailVerification')

        # absurl = 'http://'+current_site + relativeLink
        # email_body = 'Hello, \n Use link below to verify your email  \n' + absurl +"?uidb64=" + uidb64 + "&token=" + token
        # data = {'email_body': email_body, 'to_emails': [user.email,],'email_subject': 'Verify Email'} '''

        data = temp_url(request, user, reverse_name='verify-email', mail_body='verify email')

        send_email(data)

        return Response({'message': 'url sent to your email address'}, status=status.HTTP_202_ACCEPTED)
    
    def post(request):
        uidb64, token = request.GET.get('uidb64'), request.GET.get('token')
        if uidb64 is None or token is None:
            return Response({'failed':'wrong url please use the url sent to your email'},status=status.HTTP_404_NOT_FOUND)

        id = smart_str(urlsafe_base64_decode(uidb64))

        try:
            user = User.objects.get(id=id)
        except:
            return Response({'failed':'User not Found'},status=status.HTTP_404_NOT_FOUND)

        if user is not None and account_activation_token.check_token(user, token):
            user.is_email_verified = True
            user.save()
            login(request, user)
            return redirect('profile')
        else:
            # invalid link
            return Response({'message': 'wrong url'}, status=status.HTTP_400_BAD_REQUEST)
        
class PasswordForgetView(APIView):

    permission_classes=[AllowAny,]

    def get(self, request):
        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            ''' # uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            # token = PasswordResetTokenGenerator().make_token(user)
            # current_site = get_current_site(
            #     request=request).domain

            # relativeLink = reverse('forget-password',)

            # absurl = 'http://'+current_site + relativeLink

            # email_body = 'Hello, \n Use the link below to reset your password  \n' + \
            #     absurl+"?uidb64="+str(uidb64)+"&token="+str(token) 
                
            # data = {'email_body': email_body, 'to_emails': [user.email,],
            #     'email_subject': 'Reset your passsword'} '''

            data = temp_url(request, user, reverse_name={'forget-password'}, mail_body='reset password')

            send_email(data)

            return Response({'success': 'a link to reset your password sent'}, status=status.HTTP_200_OK)
        else:
            return Response({'failed':'User not Found'},status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request):
        uidb64, token = request.GET.get('uidb64'), request.GET.get('token')

        if uidb64 is None or token is None:
            return Response({'failed':'wrong url please use the url sent to your email'},status=status.HTTP_404_NOT_FOUND)

        id = smart_str(urlsafe_base64_decode(uidb64))
        try:
            user = User.objects.get(id=id)
        except:
            return Response({'failed':'User not Found'},status=status.HTTP_404_NOT_FOUND)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'failed':'Invalid token'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = ResetPasswordSerializer(data = request.data)

        if serializer.is_valid():
            user.set_password(serializer.data.get("new_password"))
            user.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordChangeView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = self.get_object()
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"message": "password updated successfully"})
        else:
            return Response({"message": "failed", "details": serializer.errors})



# user crud views

'''
class RegisterView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = UserRegisterSerializer(data = data)
            if serializer.is_valid():
                user = serializer.save()
                mail_data = temp_url(request, user, reverse_name={'verify-email'}, mail_body='verify email')
                send_email(mail_data)

                return Response({
                    'status':200,
                    'message':'registered succesfully check email',
                    'data':serializer.data,
                })
            
            return Response({
                'status':400,
                'message':'something went wrong',
                'data': serializer.errors
            })
        
        except Exception as e:
            return Response({'message': f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileDetailView(RetrieveAPIView):
    queryset           = User.objects.all()
    serializer_class   = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

class UserProfileListView(ListAPIView):
    queryset           = User.objects.all()
    serializer_class   = UserProfileSerializer
    permission_classes = (IsStaffUser,)

class ProfileUpdateView(UpdateAPIView):
    serializer_class=UserProfileUpdateSerializer
    permission_classes=[IsOwnerProfile,]
'''



# alternative user crud viewset

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    def get_permissions(self):

        if self.action in ['partial_update', 'update', 'destroy', ]:
            permission_classes = [IsAuthenticated, IsOwnerProfile,]
        else:
            permission_classes = [AllowAny,]

        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return UserProfileSerializer
        elif self.action in ['update', 'partial_update']:
            return UserProfileUpdateSerializer
        elif self.action == 'create':
            return UserRegisterSerializer

    def create(self, request,*args, **kwargs):
        try:
            serializer = self.get_serializer_class()(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                mail_data = temp_url(request, user, reverse_name="verify-email", mail_body='verify email')
                send_email(mail_data)

                return Response({
                    'status':200,
                    'message':'registered succesfully check email',
                    'data':serializer.data,
                })
            
            return Response({
                'status':400,
                'message':'something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            return Response({'message': f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


