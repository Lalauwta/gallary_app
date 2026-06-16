from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
import re

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('gallery.urls')),
]

# Serve user-uploaded media (ImageField files).
# Django's static() helper only wires up media when DEBUG=True, so in production
# (DEBUG=False) nothing served /media/ and every image 404'd. Attach the serve
# view directly so it works in every environment.
# NOTE: files live on the container disk, which Railway wipes on each redeploy —
# a persistent Volume mounted at MEDIA_ROOT (/app/media) keeps uploads across deploys.
_media_prefix = re.escape(settings.MEDIA_URL.lstrip('/'))
urlpatterns += [
    re_path(rf'^{_media_prefix}(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
