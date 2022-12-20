from django.db import models
from django.contrib.auth import get_user_model


class User(models.Model):
    name = models.CharField(max_length=50)

class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название тега')
    color = models.CharField(verbose_name='Цвет', max_length=20)
    slug = models.SlugField(verbose_name='Slug')


class Ingredient(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название ингредиента')

    def __str__(self):
        return f'{self.name}'
    

class Amount(models.Model):
    ingredient = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE, related_name='amount')
    amount = models.FloatField()
    units = models.CharField(max_length=5)


class Recipe(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='recipes', verbose_name='Автор')
    title = models.CharField(verbose_name='Название рецепта', max_length=200)
    image = models.ImageField(verbose_name='Фото блюда')
    description = models.TextField(verbose_name='Описание')
    ingredient = models.ManyToManyField(to=Amount)
    tag = models.ManyToManyField(to=Tag, related_name='recipes', verbose_name='Теги')
    time = models.IntegerField(verbose_name='Время приготовления в минутах')


class Follow(models.Model):
    follower = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name='followers', null=True)


class Favourites(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='favourites')
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)

