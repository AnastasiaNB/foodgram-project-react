from django.contrib import admin
from .models import Recipe, Ingredient, Tag, Amount

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'text')

@admin.register(Amount)
class AmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'amount', 'ingredient')
