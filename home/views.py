from django.shortcuts import render, redirect
from .models import Carousel, Themeimgs, Sponsors, SponsorDesignation
from events.models import Event
from django.contrib import messages


def registrationNotCompleted(request):
    user = request.user
    if user.is_authenticated and user.extendeduser.isProfileCompleted is False:
        messages.info(request, 'Complete your registration first.')
        return True
    return False


def home(request):
    if registrationNotCompleted(request):
        return redirect("/users/profile")
    carousel = Carousel.objects.filter(active=True)
    themes = Themeimgs.objects.all()
    featured_events = Event.objects.filter(featured=True)
    return render(request, 'home.html', {'carousel': carousel,
                                         'theme2030': themes.filter(year='2030'),
                                         'theme2040': themes.filter(year='2040'),
                                         'theme2050': themes.filter(year='2050'),
                                         'featured_events': featured_events,
                                         }
                  )


def theme(request):
    if registrationNotCompleted(request):
        return redirect("/users/profile")

    return render(request, 'theme.html')


def home_redirect(request):
    if registrationNotCompleted(request):
        return redirect("/users/profile")
    return redirect(home)

def nsd(request):
    return render(request,'nsd.html')


def sponsors(request):
    if registrationNotCompleted(request):
        return redirect("/users/profile")

    sponsorTypes = SponsorDesignation.objects.all().order_by('rank')
    sponsors = []
    for data in sponsorTypes:
        obj = {}
        obj["sponsorTypeName"] = data.sponsor_type
        obj["sponsorData"] = Sponsors.objects.filter(designation=data).all()
        if obj["sponsorData"]:
            sponsors.append(obj)
    return render(request, 'sponsors.html', {"sponsors": sponsors})
