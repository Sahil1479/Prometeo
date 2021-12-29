from django.shortcuts import render, redirect
from .models import Carousel
from django.shortcuts import get_object_or_404

def home(request):
    carousel = Carousel.objects.filter(active=True)
    return render(request, 'home.html', {'carousel': carousel})


def home_redirect(request):
    return redirect(home)
