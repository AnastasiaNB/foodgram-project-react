from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model

class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название тега')
    color = models.CharField(verbose_name='Цвет')
    slug = models.SlugField(verbose_name='Slug')


class Ingredient(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название ингредиента')
    amount = models.FloatField(verbose_name='Количество')
    units = models.CharField(verbose_name='Единицы измерения')


class Recipe(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='recipes', verbose_name='Автор')
    title = models.CharField(verbose_name='Название рецепта', max_length=200)
    image = models.ImageField(verbose_name='Фото блюда')
    description = models.TextField(verbose_name='Описание')
    ingredient = models.ManyToManyField(to=Ingredient, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(to=Tag, on_delete=models.SET_NULL, related_name='recipes', verbose_name='Теги')
    time = models.IntegerField(verbose_name='Время приготовления в минутах')


class Follow(models.Model):
    follower = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name='followers')


class Favourites(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.SET_NULL)
