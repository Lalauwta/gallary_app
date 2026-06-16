from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.home,          name='home'),
    path('upload/',             views.upload_photo,  name='upload'),
    path('photo/<int:pk>/',     views.photo_detail,  name='photo-detail'),
    path('photo/<int:pk>/delete/', views.delete_photo, name='photo-delete'),
    path('photo/<int:pk>/like/', views.like_photo,   name='photo-like'),
    path('albums/',             views.album_list,    name='album-list'),
    path('albums/<int:pk>/',    views.album_detail,  name='album-detail'),
    path('albums/create/',      views.create_album,  name='album-create'),
    path('my-photos/',          views.my_photos,     name='my-photos'),
]
