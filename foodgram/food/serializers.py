from rest_framework import serializers
from .models import Recipe, Amount, Ingredient, RecipeTags


class AmountSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Amount
        exclude = ('id', 'recipe')


class RecipeTagSerializer(serializers.ModelSerializer):
    recipe = serializers.StringRelatedField(many=True)
    tag = serializers.StringRelatedField(many=True)

    class Meta:
        model = RecipeTags
        exclude = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=True, read_only=True)
    ingredient = AmountSerializer(many=True)

    class Meta:
        model = Recipe
        exclude = ('id',)

    def create(self, data):
        ingredients = data.pop('ingredient')
        recipe = Recipe.objects.create(**data)
        for ingerdient_amount in ingredients:
            ingredient_id = ingerdient_amount['id']
            amount = ingerdient_amount['amount']
            ingredient = Ingredient.objects.get(id=ingredient_id)
            Amount.objects.create(recipe=recipe, ingredient=ingredient, amount=amount)


class UserSerializer(serializers.ModelSerializer):
    pass



