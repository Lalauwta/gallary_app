from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Photo, Album
from .forms import PhotoUploadForm, AlbumForm


# ── Home / Gallery ────────────────────────────────────────
def home(request):
    query  = request.GET.get('q', '')
    photos = Photo.objects.select_related('owner').all()

    if query:
        photos = photos.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(owner__username__icontains=query)
        )

    return render(request, 'gallery/home.html', {
        'photos': photos,
        'query': query,
    })


# ── Photo Detail ──────────────────────────────────────────
def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'gallery/photo_detail.html', {'photo': photo})


# ── Upload Photo ──────────────────────────────────────────
@login_required
def upload_photo(request):
    form = PhotoUploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        photo = form.save(commit=False)
        photo.owner = request.user
        photo.save()
        messages.success(request, 'Photo uploaded successfully! 📸')
        return redirect('photo-detail', pk=photo.pk)

    return render(request, 'gallery/upload.html', {'form': form})


# ── Delete Photo ──────────────────────────────────────────
@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk, owner=request.user)
    if request.method == 'POST':
        photo.image.delete()
        photo.delete()
        messages.success(request, 'Photo deleted.')
        return redirect('home')
    return render(request, 'gallery/confirm_delete.html', {'photo': photo})


# ── Like / Unlike ─────────────────────────────────────────
@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)
    return redirect('photo-detail', pk=pk)


# ── Album List ────────────────────────────────────────────
def album_list(request):
    albums = Album.objects.select_related('owner').all()
    return render(request, 'gallery/album_list.html', {'albums': albums})


# ── Album Detail ──────────────────────────────────────────
def album_detail(request, pk):
    album  = get_object_or_404(Album, pk=pk)
    photos = album.photos.all()
    return render(request, 'gallery/album_detail.html', {
        'album': album,
        'photos': photos,
    })


# ── Create Album ──────────────────────────────────────────
@login_required
def create_album(request):
    form = AlbumForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        album = form.save(commit=False)
        album.owner = request.user
        album.save()
        messages.success(request, f'Album "{album.title}" created!')
        return redirect('album-detail', pk=album.pk)
    return render(request, 'gallery/create_album.html', {'form': form})


# ── My Photos ─────────────────────────────────────────────
@login_required
def my_photos(request):
    photos = Photo.objects.filter(owner=request.user)
    return render(request, 'gallery/my_photos.html', {'photos': photos})
