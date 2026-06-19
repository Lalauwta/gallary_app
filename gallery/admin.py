from django.contrib import admin
from .models import Photo, Album, Comment


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display  = ['title', 'owner', 'album', 'uploaded_at']
    list_filter   = ['album', 'uploaded_at']
    search_fields = ['title', 'owner__username']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display  = ['title', 'owner', 'created_at']
    search_fields = ['title', 'owner__username']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ['author', 'photo', 'created_at']
    list_filter   = ['created_at']
    search_fields = ['author__username', 'photo__title', 'body']
