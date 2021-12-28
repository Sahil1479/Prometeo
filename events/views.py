from django.shortcuts import render
from .models import Event
from django.shortcuts import get_object_or_404


# Create your views here.
def events(request, type):
    events = Event.objects.filter(type=type)
    return render(request, 'events.html', {'events': events, 'type': type})


def event(request, type, eventid):
    event = get_object_or_404(Event, pk=eventid)
    return render(request, 'event.html', {'event': event})
