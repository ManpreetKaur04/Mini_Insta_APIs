from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Follower, UserAction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at']
        read_only_fields = ['author'] 
        
    def create(self, validated_data):
        user = self.context['request'].user  # This grabs the logged-in user from the request context
        validated_data['author'] = user  # Set the author to the logged-in user
        return super().create(validated_data)