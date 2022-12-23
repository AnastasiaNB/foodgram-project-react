from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import RecipeViewSet, IngredientViewSet, TagViewSet

router = SimpleRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls))
]