from rest_framework import serializers
from .models import Recipe, Amount


class AmountSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Amount
        exclude = ('id', 'recipe')


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=True, read_only=True)
    ingredient = AmountSerializer(many=True)

    class Meta:
        model = Recipe
        exclude = ('id',)

    def create(self, data):
        ingredients = data.pop('ingredient')
        recipe = Recipe.objects.create(**data)
        for ingredient 


class UserSerializer(serializers.ModelSerializer):
    pass



