from django import forms
from .models import Photo, Album


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model  = Photo
        fields = ['title', 'description', 'image', 'album']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Photo title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your photo...',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'album': forms.Select(attrs={
                'class': 'form-select',
            }),
        }


class AlbumForm(forms.ModelForm):
    class Meta:
        model  = Album
        fields = ['title', 'description', 'cover_photo']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Album name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'cover_photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
