from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (CustomCreateUserSerializer, CustomUserSerializer,
                          FavoriteSerializer, FollowCreateSerializer,
                          FollowSerializer, IngredientSerializer,
                          RecipeGETSerializer, RecipePOSTSerializer,
                          ShoppingCartSerializer, TagSerializer)
from food.models import (Amount, Favorites, Ingredient, Recipe, ShoppingCart,
                         Tag)
from users.models import Follow, User


class PostDeleteViewSet(viewsets.mixins.CreateModelMixin,
                        viewsets.mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
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
        return RecipePOSTSerializer

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        final_list = []
        ingredients = Amount.objects.filter(
            recipe__in_shopping_cart__user=request.user
            ).select_related('ingredient', 'recipe').values(
                'recipe__name', 'ingredient__measurement_unit').annotate(
                    Sum('amount'))
        for item in ingredients:
            final_list.append(
                f"{item['recipe__name']}, \
                    {item['amount__sum']}, \
                        {item['ingredient__measurement_unit']}")
        response = HttpResponse(
            final_list,
            content_type='application/text charset=utf-8')
        response[
            'Content-Disposition'
            ] = 'attachment; filename="shopping_cart.txt"'
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
        get_object_or_404(
            ShoppingCart,
            user=request.user,
            recipe_id=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.action == 'create':
            return CustomCreateUserSerializer
        return CustomUserSerializer

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        authors = self.paginate_queryset(
            User.objects.filter(following__follower=request.user))
        serializer = FollowSerializer(
            authors,
            context={'request': request},
            many=True)
        return self.get_paginated_response(serializer.data)


class FollowPostDeleteViewSet(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=id)
        follower = self.request.user
        data = {'follower': follower.id, 'user': user.id}
        serializer = FollowCreateSerializer(
            data=data,
            context={'request': request})
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
