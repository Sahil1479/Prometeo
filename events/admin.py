from django.contrib import admin
from .models import Event, Contacts
from django.utils.translation import ugettext_lazy as _


class ContactsAdmin(admin.StackedInline):
    model = Contacts


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'venue', 'registration_open', 'type')
    list_filter = ('type', 'registration_open')
    search_fields = ['name']
    inlines = [ContactsAdmin, ]
    fieldsets = (
        (_('Event Details'), {'fields': ('name', 'type', 'speaker', 'description', 'problem_statement', 'rulebook_text', 'prize', 'external_link', 'venue', 'featured')}),
        (_('Event Registration Details'), {'fields': ('participation_type', 'min_team_size', 'max_team_size', 'registration_open')}),
        (_('Event Dates'), {'fields': ('date', 'time', 'end_date', 'end_time', 'event_started')}),
        (_('Event Host'), {'fields': ('host', 'sponsor_image1', 'sponsor_website')}),
        (_('Event Links'), {'fields': ('meet_link', 'youtube_link', 'webx_link')}),
        (_('Event Uploads'), {'fields': ('image', 'rulebook')}),
    )


admin.site.register(Event, EventAdmin)
