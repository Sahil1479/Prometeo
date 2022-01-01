from django.shortcuts import render, redirect
from .models import Carousel


def home(request):
    user = request.user
    if user.is_authenticated and user.extendeduser.isProfileCompleted == False:
        # In that case, the user must have to complete its profile first.
        return redirect("/users/profile")
        
    carousel = Carousel.objects.filter(active=True)
    return render(request, 'home.html', {'carousel': carousel})


def home_redirect(request):
    return redirect(home)
