from django.shortcuts import render, redirect
from .models import Carousel,Themeimgs
from django.shortcuts import get_object_or_404

def home(request):
    carousel = Carousel.objects.filter(active=True)
    themes=Themeimgs.objects.all()
    return render(request, 'home.html', {'carousel': carousel,
    'theme2030':themes.filter(year='2030'),
    'theme2040':themes.filter(year='2040'),
    'theme2050':themes.filter(year='2050'),
    })


def home_redirect(request):
    return redirect(home)
