from django.urls import path
from .views import home
from .views import theme

app_name = 'home'

urlpatterns = [
    path('', home, name='home'),
    path('theme/', theme, name='theme'),
]
