from rest_framework import serializers
from account.models import User
from django.contrib.auth.hashers import check_password


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', ]


    def validate_password(self, data):
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError("passwords should match")
        return data

    def create(self, validated_data):
        user = User(
        email=validated_data['email'],
        username=validated_data['username'],)
        user.set_password(validated_data['password'])
        user.save()

        return user


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirmed_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirmed_password']:
            raise serializers.ValidationError("passwords should match")
        return data
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirmed_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context['request'].user
        if not check_password(data['old_password'], user.password):
            raise serializers.ValidationError({'old_password': 'Wrong password.'})
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({'new_password': 'new password should not match with old password'})
        if data['new_password'] != data['confirmed_password']:
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
