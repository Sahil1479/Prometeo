from django.shortcuts import render
from .models import Coordinator, Designation


def coordinator(request):
    teamTypes = Designation.objects.all().order_by('rank')
    our_team = []
    for data in teamTypes:
        obj = {}
        obj["teamName"] = data.designationName
        obj["teamData"] = Coordinator.objects.filter(team=data).all()
        if obj["teamData"]:
            our_team.append(obj)
    return render(request, "coordinator.html", {"ourTeam": our_team})
