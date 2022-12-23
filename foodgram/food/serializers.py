from rest_framework import serializers
from .models import Recipe, Amount, Ingredient, RecipeTags, Tag, Favorites, ShoppingCart


class AmountSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Amount
        field = '__all__'


class RecipeTagSerializer(serializers.ModelSerializer):
    recipe = serializers.StringRelatedField(many=True)
    tag = serializers.StringRelatedField(many=True)

    class Meta:
        model = RecipeTags
        field = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measure_units = serializers.SerializerMethodField()

    class Meta:
        model = Amount
        exclude = ('recipe', )

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measure_units(self, obj):
        return obj.ingredient.measure_units

    def get_id(self, obj):
        return obj.ingradient.id


class RecipePOSTSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    ingredients = AmountSerializer(many=True)
    tag = RecipeTagSerializer(many=True)
    image = serializers.ImageField()

    class Meta:
        model = Recipe
        field = '__all__'

    def create(self, data):
        ingredients = data.pop('ingredients')
        tags = data.pop('tags')
        recipe = Recipe.objects.create(**data)
        for ingerdient_amount in ingredients:
            ingredient_id = ingerdient_amount['id']
            amount = ingerdient_amount['amount']
            ingredient = Ingredient.objects.get(id=ingredient_id)
            Amount.objects.create(recipe=recipe, ingredient=ingredient, amount=amount)
        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            RecipeTags.objects.create(recipe=recipe, tag=tag)


class RecipeGETSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        ingredients = Amount.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        return Favorites.objects.filter(recipe=obj, user=obj.author).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(recipe=obj, user=obj.author).exists()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    pass



