from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from food.models import Recipe, Amount, Ingredient, Tag, Favorites, ShoppingCart, User




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class AmountSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для создания и отображения ингредиентов рецепта."""
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(source='ingredient', queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(write_only=True, min_value=1)
    measure_units = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Amount
        fields = ('id', 'name', 'measure_units', 'amount', 'recipe')

    def get_measure_units(self, obj):
        ingredient = Ingredient.objects.get(id=obj.id)
        return ingredient.measurement_unit

    def get_name(self, obj):
        ingredient = Ingredient.objects.get(id=obj.id)
        return ingredient.name

    def to_representation(self, obj):
        self.fields.pop('recipe')
        representation = super().to_representation(obj)
        representation['amount'] = obj.amount
        return representation


class RecipePOSTSerializer(serializers.ModelSerializer):
    """Серализатор для POST-запросов к адресу api/recipes/"""
    author = UserSerializer(required=False)
    ingredients = AmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,queryset=Tag.objects.all())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'

    # def validate(self, data):
      #  request = self.context.get('request')
       # user = request.user
        #if user.is_anonymous:
         #   return False  

    def create(self, data):
        # author = self.context.get('request').user
        ingredients = data.pop('ingredients')
        tags = data.pop('tags')
        recipe = Recipe.objects.create(**data)
        recipe.tags.set(tags)
        for ingerdient_amount in ingredients:
            amount = ingerdient_amount['amount']
            Amount.objects.create(recipe=recipe, ingredient=ingerdient_amount['ingredient'], amount=amount)
        recipe.save()
        return recipe

    def update(self, obj, data):
        ingredients = data.pop('ingredients')
        tags = data.pop('tags')
        obj.tags.clear()
        Amount.objects.filter(recipe=obj).delete()
        obj.tags.set(tags)
        for ingerdient_amount in ingredients:
            amount = ingerdient_amount['amount']
            Amount.objects.create(recipe=obj, ingredient=ingerdient_amount['ingredient'], amount=amount)
        obj.save()
        return super().update(obj, data)

    def to_representation(self, obj):
        self.fields.pop('ingredients')
        representation = super().to_representation(obj)
        representation['ingredients'] = AmountSerializer(
            Amount.objects.filter(recipe=obj).all(), many=True
        ).data
        return representation


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов (запросы к api/tags/)"""
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('__all__',)


class RecipeGETSerializer(serializers.ModelSerializer):
    """Серализатор для GET-запросов к адресу api/recipes/"""
    author = serializers.StringRelatedField(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        ingredients = Amount.objects.filter(recipe=obj)
        return AmountSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        return Favorites.objects.filter(recipe=obj, user=obj.author).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(recipe=obj, user=obj.author).exists()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов (запросы к api/ingredients/)"""
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('__all__',)


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для изранного"""
    user = serializers.SerializerMethodField()
    recipe = serializers.SerializerMethodField()
    class Meta:
        model = Favorites
        fields = '__all__'

    def get_user(self, obj, data):
        user_id = data['user']
        return User.objects.get(id=user_id)

    def get_recipe(self, obj, data):
        recipe_id = obj
        return Recipe.objects.get(id=recipe_id)










