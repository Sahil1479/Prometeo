from django.contrib import admin
from .models import Designation, Coordinator


@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'email', 'phoneNo']

    class Meta:
        model = Coordinator
        fields = '__all__'


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ['designationName', ]

    class Meta:
        model = Designation
        fields = '__all__'
