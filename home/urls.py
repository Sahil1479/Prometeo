from django.urls import path
from .views import home, theme, sponsors, nsd

app_name = 'home'

urlpatterns = [
    path('', home, name='home'),
    path('theme/', theme, name='theme'),
    path('sponsors/', sponsors, name='sponsors'),
    path('nsd/', nsd, name='nsd'),
]
