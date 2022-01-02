from django.contrib import admin
from .models import Carousel, Themeimgs


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', ]
    list_filter = ['active', ]

    class Meta:
        model = Carousel
        fields = '__all__'


admin.site.register(Themeimgs)
