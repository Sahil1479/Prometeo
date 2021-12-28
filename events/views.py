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


# @login_required
# def registered(request):
#     events = request.user.events.all()
#     types = ['technical', 'informal', 'workshop']
#     categories = []
#     for type in types:
#         if(request.user.events.filter(type=type).exists()):
#             categories.append(type)
#     return render(request, 'registered.html', {'events' : events, 'categories':categories})

# @login_required
# def register_for_event(request, eventid):
#     event = Event.objects.get(pk=eventid)
#     if(not event.registration_open):
#         return redirect('event', event.type, event.pk)
#     request.user.events.add(event)
#     messages.success(request, f"Successfully registered for '{event.name}'.")
#     return redirect(user_profile)
