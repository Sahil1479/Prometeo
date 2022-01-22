from django.shortcuts import render
from .models import Event
from django.shortcuts import get_object_or_404
from datetime import date, datetime


# Create your views here.
def events(request, type):
    events = Event.objects.all()
    today = date.today()
    if type == 'Live':
        liveevents = Event.objects.filter(end_date__gte=today).filter(date__lte=today).filter(event_started=True).order_by('time')
        print(liveevents)
        return render(request, 'liveevents.html', {'liveevents': liveevents, 'type': type,
                                                   'present_time': datetime.now(),
                                                   })
    else:
        return render(request, 'events.html', {'events': events, 'type': type})


def event(request, type, eventid):
    event = get_object_or_404(Event, pk=eventid)
    return render(request, 'event.html', {'event': event})


def schedule(request):
    day1 = Event.objects.filter(date="2022-01-20").order_by('time')
    day2 = Event.objects.filter(date="2022-02-27").order_by('time')
    day3 = Event.objects.filter(date="2022-02-28").order_by('time')
    day4 = Event.objects.filter(date="2022-03-01").order_by('time')
    return render(request, 'schedule.html', {'day1': day1, 'day2': day2, 'day3': day3, 'day4': day4})
