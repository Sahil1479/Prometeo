from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Coordinator, Designation


def coordinator(request):
    user = request.user
    if user.is_authenticated and user.extendeduser.isProfileCompleted is False:
        messages.success(request, 'Complete your profile first.')
        return redirect("/users/profile")

    teamTypes = Designation.objects.all().order_by('rank')
    our_team = []
    for data in teamTypes:
        obj = {}
        obj["teamName"] = data.designationName
        obj["teamData"] = Coordinator.objects.filter(team=data).all()
        if obj["teamData"]:
            our_team.append(obj)
    return render(request, "coordinator.html", {"ourTeam": our_team})
