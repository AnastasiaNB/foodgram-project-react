from django.db import models
from django.contrib.auth import get_user_model


class Units(models.Model):
    name = models.CharField(max_length=5)


class User(models.Model):
    name = models.CharField(max_length=50)

class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название тега')
    color = models.CharField(verbose_name='Цвет', max_length=20)
    slug = models.SlugField(verbose_name='Slug')


class Ingredient(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название ингредиента')
    measurement_unit = models.ForeignKey(to=Units, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='recipes', verbose_name='Автор')
    name = models.CharField(verbose_name='Название рецепта', max_length=200)
    image = models.ImageField(verbose_name='Фото блюда')
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(to=Ingredient, through='Amount', verbose_name='Ингредиенты')
    tags = models.ManyToManyField(to=Tag, related_name='recipes', verbose_name='Теги', through='RecipeTags')
    time = models.IntegerField(verbose_name='Время приготовления в минутах')
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)


class Amount(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='ingredient', null=True)
    ingredient = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE, related_name='amount')
    amount = models.FloatField()


class RecipeTags(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='tags', null=True)
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE, null=True)


class Follow(models.Model):
    follower = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name='followers', null=True)


class Favourites(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='favourites')
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)

