from django.contrib import admin

from .models import Amount, Favorites, Ingredient, Recipe, Tag 


class AmountInline(admin.StackedInline):
    model = Amount
    min_num = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [AmountInline]
    list_display = (
        'id', 'author', 'name',
        'get_favorite_count', 'get_ingredients')

    def get_ingredients(self, obj):
        return [ingredient.name for ingredient in obj.ingredients.all()]

    def get_favorite_count(self, obj):
        return obj.in_favorites.count()


@admin.register(Amount)
class AmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'amount', 'ingredient')


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
