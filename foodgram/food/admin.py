from django.contrib import admin
from .models import Recipe, Ingredient, Tag, Amount, Favorites

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'text', 'get_ingredients')

    def get_ingredients(self, obj):
        return [ingredient.name for ingredient in obj.ingredients.all()]

@admin.register(Amount)
class AmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'amount', 'ingredient')

@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')

