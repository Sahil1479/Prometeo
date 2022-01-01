from django.shortcuts import render, redirect
from .models import Team

# Create your views here.
def team(request):
    user = request.user
    if user.is_authenticated and user.extendeduser.isProfileCompleted == False:
        # In that case, the user must have to complete its profile first.
        return redirect("/users/profile")
    teams = Team.objects.all()
    teamTypes = []
    for team in teams:
        if team.team not in teamTypes:
            teamTypes.append(team.team)
    print(teamTypes)
    our_team = []
    for data in teamTypes:
        obj = {}
        obj["teamName"] = data
        obj["teamData"] = Team.objects.filter(team=data).all()
        our_team.append(obj)
    return render(request, "team.html", {"ourTeam" : our_team})