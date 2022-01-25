from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('coordinator/', include('coordinator.urls')),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns = urlpatterns + [url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})]

