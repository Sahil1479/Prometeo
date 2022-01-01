from django.contrib import admin
from .models import Event


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'venue', 'registration_open', 'type')
    list_filter = ('type', 'registration_open')
    search_fields = ['name']


admin.site.register(Event, EventAdmin)
