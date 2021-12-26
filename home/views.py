from django.shortcuts import render, redirect
from .models import Carousel


def home(request):
    carousel = Carousel.objects.filter(active=True)
    return render(request, 'home.html', {'carousel': carousel})


def home_redirect(request):
    return redirect(home)
