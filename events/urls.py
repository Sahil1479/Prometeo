from django.urls import path
from .views import event, events, schedule, uploadSubmission

app_name = 'events'
urlpatterns = [
    path('schedule/', schedule, name="schedule"),
    path('<slug:type>/', events, name="events"),
    path('<slug:type>/<int:eventid>/', event, name="event"),
    path('submission', uploadSubmission, name='uploadSubmission')
]
