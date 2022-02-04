from django.shortcuts import render, redirect
from .models import Brochure, Event
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import date, datetime
from .models import EVENT_CHOICES, Panel


def registrationNotCompleted(request):
    user = request.user
    if user.is_authenticated and user.extendeduser.isProfileCompleted is False:
        messages.info(request, 'Complete your registration first.')
        return True
    return False

# Create your views here.


def events(request, type):
    if registrationNotCompleted(request):
        return redirect("/users/profile")

    events = Event.objects.all()
    today = date.today()
    brochure = Brochure.objects.filter(type=type).first()
    if type == 'live':
        liveevents = Event.objects.filter(end_date__gte=today).filter(date__lte=today).filter(event_started=True).order_by('time')
        return render(request, 'liveevents.html', {'liveevents': liveevents, 'type': type,
                                                   'present_time': datetime.now(),
                                                   })
    elif type == 'talk':
        events = Event.objects.filter(type=type)
        return render(request, 'speakers.html', {'events': events, 'type': type, 'brochure': brochure, })
    elif type == 'panel_discussion':
        events = Event.objects.filter(type=type)
        panelist = Panel.objects.all()
        return render(request, 'panel.html', {'events': events, 'panelists': panelist, 'type': type})
    else:
        typeFound = False
        for item in EVENT_CHOICES:
            if type == item[0]:
                typeFound = True
        if typeFound is False:
            messages.info(request, 'No event type exists with the given name.')
            return redirect("/")
        events = Event.objects.filter(type=type)
        return render(request, 'events.html', {'events': events, 'type': type, 'brochure': brochure, })


def event(request, type, eventid):
    if registrationNotCompleted(request):
        return redirect("/users/profile")
    event = get_object_or_404(Event, pk=eventid)
    return render(request, 'event.html', {'event': event})


def schedule(request):
    if registrationNotCompleted(request):
        return redirect("/users/profile")
    schedule_file = Brochure.objects.filter(type='schedule_file').first()
    day1 = Event.objects.filter(date="2022-02-26").order_by('time')
    day2 = Event.objects.filter(date="2022-02-27").order_by('time')
    day3 = Event.objects.filter(date="2022-02-28").order_by('time')
    day4 = Event.objects.filter(date="2022-03-01").order_by('time')
    return render(request, 'schedule.html', {'day1': day1, 'day2': day2, 'day3': day3, 'day4': day4, 'schedule_file': schedule_file, })
