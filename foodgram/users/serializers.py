from djoser.serializers import UserSerializer
from rest_framework import serializers
from .models import User, Follow


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователей"""
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name') 


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов к api/users/subscriptions/"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    # def get_recipes(self, obj):
      #  user_id = obj.recipes