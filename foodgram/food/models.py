from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название тега')
    color = models.CharField(verbose_name='Цвет', max_length=20)
    slug = models.SlugField(verbose_name='Slug')


class Ingredient(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=10, default='г')


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', verbose_name='Автор', null=True)
    name = models.CharField(verbose_name='Название рецепта', max_length=200)
    image = models.ImageField(verbose_name='Фото блюда', upload_to='food/images')
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(Ingredient, through='Amount', verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, related_name='recipes', verbose_name='Теги')
    cooking_time = models.IntegerField(verbose_name='Время приготовления в минутах')
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)


class Amount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient', null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='amount')
    amount = models.IntegerField()


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='favorite')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)

class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='in_shopping_cart')

