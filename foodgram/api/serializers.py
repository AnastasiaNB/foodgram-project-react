from djoser.serializers import (UserCreateSerializer,
                                UserSerializer)
from drf_extra_fields.fields import Base64ImageField

from food.models import (Amount, Favorites, Ingredient, Recipe, ShoppingCart,
                         Tag)
from rest_framework import serializers

from users.models import Follow, User


class CustomCreateUserSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователей"""
    class Meta:
        model = User
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'password',
            )


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


class AmountSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для создания
     и отображения ингредиентов рецепта."""
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all())
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
        representation = super().to_representation(obj)
        representation['amount'] = obj.amount
        return representation


class RecipePOSTSerializer(serializers.ModelSerializer):
    """Серализатор для POST-запросов к адресу api/recipes/"""
    author = CustomUserSerializer(read_only=True)
    ingredients = AmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return data

    def create(self, data):
        author = self.context.get('request').user
        ingredients = data.pop('ingredients')
        tags = data.pop('tags')
        recipe = Recipe.objects.create(author=author, **data)
        recipe.tags.set(tags)
        Amount.objects.bulk_create([Amount(
                recipe=recipe,
                ingredient=ingerdient_amount['ingredient'],
                amount=ingerdient_amount['amount']
                ) for ingerdient_amount in ingredients])
        recipe.save()
        return recipe

    def update(self, obj, data):
        ingredients = data.pop('ingredients')
        tags = data.pop('tags')
        obj.tags.clear()
        Amount.objects.filter(recipe=obj).delete()
        obj.tags.set(tags)
        Amount.objects.bulk_create([Amount(
                recipe=obj,
                ingredient=ingerdient_amount['ingredient'],
                amount=ingerdient_amount['amount']
                ) for ingerdient_amount in ingredients])
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
    author = CustomUserSerializer(read_only=True)
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
        if self.context.get('request').user.is_anonymous:
            return False
        return Favorites.objects.filter(
            recipe=obj,
            user=self.context.get('request').user).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            recipe=obj,
            user=self.context.get('request').user).exists()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов (запросы к api/ingredients/)"""
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('__all__',)


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранного"""
    id = serializers.ReadOnlyField(source='recipe.id',)
    name = serializers.ReadOnlyField(source='recipe.name',)
    image = serializers.CharField(source='recipe.image', read_only=True,)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time',)

    class Meta:
        model = Favorites
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        user = self.context.get('request').user
        recipe = self.context.get('recipe_id')
        if Favorites.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Рецепт уже в избранном'})
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок"""
    id = serializers.ReadOnlyField(source='recipe.id',)
    name = serializers.ReadOnlyField(source='recipe.name',)
    image = serializers.CharField(source='recipe.image', read_only=True,)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time',)

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        user = self.context.get('request').user
        recipe = self.context.get('recipe_id')
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Рецепт уже в корзине'})
        return data


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов к api/users/subscriptions/"""
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Follow.objects.filter(user=obj, follower=request.user).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj)[:int(recipes_limit)]
        serializer = ShortRecipeSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class FollowCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('user', 'follower')

    def to_representation(self, obj):
        request = self.context.get('request')
        context = {'request': request}
        serializer = FollowSerializer(obj.user, context=context)
        return serializer.data

    def validate(self, data):
        user = data.get('user')
        follower = data.get('follower')
        if user == follower:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        if Follow.objects.filter(follower=follower, user=user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя'
            )
        return data
