from djoser.serializers import (UserCreateSerializer,
                                UserSerializer)

from rest_framework import serializers

from users.models import User, Follow


class CustomUserSerializer(UserSerializer):
    """Сериализатор для получения пользователей"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, follower=obj.id).exists()


class CustomCreateUserSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователей"""
    class Meta:
        model = User
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'password',
            )