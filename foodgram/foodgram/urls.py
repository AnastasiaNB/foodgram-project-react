from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('food.urls')),
    path('follow/', include('food.urls')),
    path('favourites/', include('food.urls')),
    path('shoping_list/', include('food.urls')),
    path('recipe/<pk>/')
]
