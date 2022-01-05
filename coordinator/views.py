from django.shortcuts import render
from .models import Coordinator


def coordinator(request):
    teams = Coordinator.objects.all()
    teamTypes = []
    for team in teams:
        if team.team not in teamTypes:
            teamTypes.append(team.team)
    print(teamTypes)
    our_team = []
    for data in teamTypes:
        obj = {}
        obj["teamName"] = data
        obj["teamData"] = Coordinator.objects.filter(team=data).all()
        our_team.append(obj)
    return render(request, "coordinator.html", {"ourTeam": our_team})
