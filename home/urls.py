from django.urls import path
from .views import home, theme, sponsors, nsd, privacyPolicy, streamLinks
from django.shortcuts import redirect

app_name = 'home'

urlpatterns = [
    path('', home, name='home'),
    path('theme/', theme, name='theme'),
    path('sponsors/', sponsors, name='sponsors'),
    path('national-science-day/', nsd, name='nsd'),
    path('privacy-policy/', privacyPolicy, name='privacy-policy'),
    path('venue/', lambda request: redirect('/events/schedule', permanent=False)),
    path('venue/<slug:type>', streamLinks, name='streamLinks')
]
