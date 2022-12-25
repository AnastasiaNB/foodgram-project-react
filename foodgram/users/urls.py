from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import UserViewSet


router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('', include('users.urls')),
    path('', include('djoser.urls'))
]