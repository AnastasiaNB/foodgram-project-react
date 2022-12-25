from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from food.models import Recipe, Ingredient, Tag, Favorites
from .serializers import RecipePOSTSerializer, RecipeGETSerializer, IngredientSerializer,TagSerializer, FavoriteSerializer

class PostDeleteViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    pass


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipePOSTSerializer
    permission_classes = [AllowAny, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGETSerializer
        else:
            return RecipePOSTSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]


class FavoriteViewSet(PostDeleteViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [AllowAny, ]

