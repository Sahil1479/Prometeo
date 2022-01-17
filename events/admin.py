from pyexpat import model
from django.contrib import admin
from .models import Event, Contacts


class ContactsAdmin(admin.StackedInline):
    model = Contacts

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'venue', 'registration_open', 'type')
    list_filter = ('type', 'registration_open')
    search_fields = ['name']
    inlines = [ContactsAdmin, ]


admin.site.register(Event, EventAdmin)
