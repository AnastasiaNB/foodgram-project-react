from django.contrib import admin
from .models import Follow, User


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'follower')


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email',
        'first_name', 'last_name')
    list_filter = ('username', 'email')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
