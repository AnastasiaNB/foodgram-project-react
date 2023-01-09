from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CustomUserViewSet, FavoriteViewSet,
                    FollowPostDeleteViewSet, IngredientViewSet, RecipeViewSet,
                    ShoppingCartViewSet, TagViewSet)

router = SimpleRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register(r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet, basename='favorite')
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart', ShoppingCartViewSet, basename='shoppingcart')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:user_id>/subscribe/', FollowPostDeleteViewSet.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]