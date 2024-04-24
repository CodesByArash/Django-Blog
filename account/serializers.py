from rest_framework import serializers
from account.models import User
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class UserRegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(required=True, write_only = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password','confirm_password']


    def validate(self, data):
        passw , c_passw = data.get('password'), data.get('confirm_password')
        if passw and c_passw:
            if passw != c_passw:
                raise serializers.ValidationError("passwords should match")
        print("validation")
        return data

    def create(self, validated_data):
        user = User(
        email=validated_data['email'],
        username=validated_data['username'],)
        user.set_password(validated_data['password'])
        user.save()
        
        print("create")

        return user


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("passwords should match")
        return data
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context['request'].user
        if not check_password(data['old_password'], user.password):
            raise serializers.ValidationError({'old_password': 'Wrong password.'})
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({'new_password': 'new password should not match with old password'})
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({'new_password': 'new Passwords do not match.'})
        return data
    
    
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name', 'bio']

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
    default_error_messages={
        "bad_token":('token is expired or invalid')
    }
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)