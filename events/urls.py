from django.urls import path
from .views import event, events, schedule

urlpatterns = [
    path('schedule/', schedule, name="schedule"),
    path('<slug:type>/', events, name="events"),
    path('<slug:type>/<int:eventid>/', event, name="event"),
]
