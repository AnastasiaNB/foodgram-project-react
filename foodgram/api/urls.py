from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import RecipeViewSet, IngredientViewSet, TagViewSet, FavoriteViewSet

router = SimpleRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register(r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
]