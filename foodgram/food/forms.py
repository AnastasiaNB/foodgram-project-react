from models import Recipe
from django import forms


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        field = ['title', 'image', 'description', 'ingredient', 'time', 'tag']
        labels = {
            'title': 'Название блюда',
            'image': 'Фото блюда',
            'description':'Описание рецепта',
            'ingredient': 'Ингредиенты',
            'time': 'Время приготовления',
            'tag':'Теги'
        }