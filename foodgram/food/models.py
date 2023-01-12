from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название тега')
    color = models.CharField(verbose_name='Цвет', max_length=20)
    slug = models.SlugField(verbose_name='Slug')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return str(self.name)


class Ingredient(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=10, default='г')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='name-units')]

    def __str__(self):
        return str(self.name)


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор', null=True)
    name = models.CharField(verbose_name='Название рецепта', max_length=200)
    image = models.ImageField(
        verbose_name='Фото блюда',
        upload_to='food/images')
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Amount',
        verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[MinValueValidator(1)])
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return str(self.name)


class Amount(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='ingredient', null=True)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='amount')
    amount = models.IntegerField()

    class Meta:
        verbose_name = 'Рецепт-ингредиент'
        verbose_name_plural = 'Рецепты-ингредиенты'


class Favorites(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True,
        related_name='favorite')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, null=True,
        related_name='in_favorites')

    class Meta:
        verbose_name = 'Рецепт в избранном'
        verbose_name_plural = 'Рецепты в избранном'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_cart')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='in_shopping_cart')

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
