from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('coordinator/', include('coordinator.urls')),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
