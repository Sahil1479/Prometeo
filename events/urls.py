from django.urls import path
from .views import *

app_name='events'
urlpatterns = [
    path('<slug:type>/', events, name="events"),
    path('<slug:type>/<int:eventid>/', event, name="event"),
    
] 

