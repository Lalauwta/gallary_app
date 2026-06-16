from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('gallery.urls')),
]

# Serve media files during development or when explicitly enabled in production
serve_media = getattr(settings, 'DEBUG', False) or os.environ.get('SERVE_MEDIA', 'False') == 'True'
if serve_media:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
