from django.contrib import admin
from .models import Post, Follower, UserAction

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)

@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')
    search_fields = ('follower__username', 'following__username')
    list_filter = ('follower', 'following')

@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_user', 'action')
    search_fields = ('user__username', 'target_user__username')
    list_filter = ('action',)
