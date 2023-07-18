from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User,FriendRequest
from django.contrib.auth.hashers import make_password
# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password']

    def post(self, validated_data):
    	validated_data['password'] = make_password(validated_data['password'])
    	instance = User.objects.create(**validated_data)
    	return instance

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'created_at', 'is_accepted']
        read_only_fields = ['id', 'from_user', 'to_user', 'created_at']
