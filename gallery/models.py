from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    cover_photo = models.ImageField(upload_to='covers/', null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def photo_count(self):
        return self.photos.count()


class Photo(models.Model):
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    album       = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')
    image       = models.ImageField(upload_to='photos/%Y/%m/')
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes       = models.ManyToManyField(User, blank=True, related_name='liked_photos')

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()
