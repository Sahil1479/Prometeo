from dataclasses import fields
from tabnanny import verbose
from django.contrib import admin
from .models import Carousel, Themeimgs, Sponsors, SponsorDesignation


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', ]
    list_filter = ['active', ]

    class Meta:
        model = Carousel
        fields = '__all__'


@admin.register(Themeimgs)
class ThemeimgsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year', ]

    class Meta:
        model = Themeimgs
        fields = '__all__'

class SponsorsAdmin(admin.StackedInline):
    model = Sponsors
    list_display = ['name']
    
    class Meta:
        model = Sponsors
        fields = '__all__'

class SponsorsDesignationAdmin(admin.ModelAdmin):
    model = SponsorDesignation
    list_display = ['sponsor_type']
    inlines = [SponsorsAdmin, ]

    class Meta:
        model = Sponsors
        fields = '__all__'

admin.site.register(SponsorDesignation, SponsorsDesignationAdmin)