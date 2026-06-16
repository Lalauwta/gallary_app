from django.contrib import admin
from .models import Photo, Album


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display  = ['title', 'owner', 'album', 'uploaded_at']
    list_filter   = ['album', 'uploaded_at']
    search_fields = ['title', 'owner__username']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display  = ['title', 'owner', 'created_at']
    search_fields = ['title', 'owner__username']
