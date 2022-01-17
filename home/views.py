from django.shortcuts import render, redirect
from .models import Carousel, Themeimgs
from django.contrib import messages


def home(request):
    user = request.user
    if user.is_authenticated and user.extendeduser.isProfileCompleted is False:
        messages.success(request, 'Complete your profile first.')
        return redirect("/users/profile")
    carousel = Carousel.objects.filter(active=True)
    themes = Themeimgs.objects.all()
    return render(request, 'home.html', {'carousel': carousel,
                                         'theme2030': themes.filter(year='2030'),
                                         'theme2040': themes.filter(year='2040'),
                                         'theme2050': themes.filter(year='2050'),
                                         }
                  )


def theme(request):
    user = request.user
    if user.is_authenticated and user.extendeduser.isProfileCompleted is False:
        messages.success(request, 'Complete your profile first.')
        return redirect("/users/profile")

    return render(request, 'theme.html')


def home_redirect(request):
    user = request.user
    if user.is_authenticated and user.extendeduser.isProfileCompleted is False:
        messages.success(request, 'Complete your profile first.')
        return redirect("/users/profile")
    return redirect(home)
