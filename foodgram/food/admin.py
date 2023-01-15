from django.contrib import admin

from .models import Amount, Favorites, Ingredient, Recipe, Tag, ShoppingCart


class AmountInline(admin.StackedInline):
    model = Amount
    min_num = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [AmountInline]
    list_display = (
        'id', 'author', 'name',
        'favorite_count', 'get_ingredients')
    readonly_fields = ('favorite_count', )
    exclude = ('is_favorited', 'is_in_shopping_cart', )
    list_filter = ('author', 'name', 'tags')

    def get_ingredients(self, obj):
        return [ingredient.name for ingredient in obj.ingredients.all()]
    get_ingredients.short_description = 'Ингредиенты'

    def favorite_count(self, obj):
        return obj.in_favorites.count()
    favorite_count.short_description = 'Добавления в избранное'


@admin.register(Amount)
class AmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'amount', 'ingredient')


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
