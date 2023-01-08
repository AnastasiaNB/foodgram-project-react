from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from rest_framework import status, views

from food.models import Recipe, Ingredient, Tag, Favorites, ShoppingCart, Amount
from users.models import User, Follow
from .pagination import CustomPagination
from .filters import RecipeFilter, IngredientFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    RecipePOSTSerializer,
    RecipeGETSerializer,
    IngredientSerializer,
    TagSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
    CustomUserSerializer,
    CustomCreateUserSerializer,
    FollowSerializer,
    FollowCreateSerializer
    )

class PostDeleteViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    pass


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGETSerializer
        else:
            return RecipePOSTSerializer
            
    @action(detail=False, methods=['get'], permission_classes = [IsAuthenticated])
    def download_shopping_cart(self, request):
        final_list = {}
        ingredients = Amount.objects.filter(
            recipe__in_shopping_cart__user=request.user)
        for item in ingredients:
            name = item.ingredient.name
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': item.ingredient.measurement_unit,
                    'amount': item.amount
                }
            else:
                final_list[name]['amount'] += item.amount
        response = HttpResponse(final_list.items(), content_type='application/text charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
        return response


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [IngredientFilter]
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]


class FavoriteViewSet(PostDeleteViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.id
        return Favorites.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(
                Recipe,
                id=self.kwargs.get('recipe_id')
            )
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        get_object_or_404(
            Favorites,
            user=request.user,
            recipe_id=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(PostDeleteViewSet):
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.id
        return ShoppingCart.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(
                Recipe,
                id=self.kwargs.get('recipe_id')
            )
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        get_object_or_404(ShoppingCart, user=request.user, recipe_id=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.action == 'create':
            return CustomCreateUserSerializer
        return CustomUserSerializer

    @action(methods=['get'], detail=False, pagination_class=CustomPagination)
    def subscriptions(self, request):
        authors = User.objects.filter(following__follower=request.user)
        serializer = FollowSerializer(authors, context={'request': request}, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        

class FollowPostDeleteViewSet(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=id)
        follower = self.request.user
        data = {'follower': follower.id, 'user': user.id}
        serializer = FollowCreateSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=id)
        follower = self.request.user
        follow = get_object_or_404(Follow, user=user, follower=follower)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)