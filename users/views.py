from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ExtendedUser, Team
from events.models import Event
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import uuid
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import TeamCreationForm, TeamJoiningForm

User = get_user_model()


@login_required
def user_profile(request):
    if(request.method == "POST"):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        college_name = request.POST['college_name']
        phone_no = request.POST['phone_no']
        gender = request.POST['gender']
        city = request.POST['city']
        current_year = request.POST['current_year']
        isCampusAmbassador = request.POST.get('isCampusAmbassador', False)
        referralCode = request.POST.get('referral_code', 'default')
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        extendeduser = ExtendedUser.objects.filter(user=request.user).first()
        # If the current user is using referral code.
        if referralCode and referralCode != "default":
            referredBy = ExtendedUser.objects.filter(invite_referral=referralCode).first()
            if referredBy:
                extendeduser.referred_by = referredBy.user
            else:
                messages.error(request, 'No referral code found, either check your code again or leave the field empty.')
                return redirect("/users/profile")
        extendeduser.gender = gender
        extendeduser.contact = phone_no
        extendeduser.current_year = gender
        extendeduser.college = college_name
        extendeduser.city = city
        extendeduser.current_year = current_year
        if isCampusAmbassador == "on":
            extendeduser.ambassador = True
        # If the user wants to be the campus ambassador.
        invite_referral = 'CA' + str(uuid.uuid4().int)[:6]
        if extendeduser.isProfileCompleted is False and extendeduser.ambassador is True:
            invite_referral = 'CA' + str(uuid.uuid4().int)[:6]
            extendeduser.invite_referral = invite_referral
            send_mail(
                'Campus Ambassador',
                f"Dear {user.first_name},\nYou are now a campus ambassador. Your referral code is {invite_referral}.\nRegards,\nPrometeo 2022 Team",
                'iitj.iotwebportal@gmail.com',
                [user.email],
                fail_silently=False,
            )
        extendeduser.isProfileCompleted = True
        extendeduser.save()
        messages.success(request, 'Your profile has been updated.')
    return render(request, 'profile.html')


@login_required
def create_team(request, eventid):
    event = get_object_or_404(Event, pk=eventid)
    if(request.user.teams.filter(event=event).exists()):
        return redirect(f'/events/{event.type}/{event.pk}')
    if request.method == 'POST':
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.id = 'PRO' + str(uuid.uuid4().int)[:6]
            team.leader = request.user
            team.event = event
            team.save()
            team.members.add(request.user)
            team.save()
            request.user.extendeduser.events.add(event)
            message = f'You have just created team "{team.name}" for the {event.type} event {event.name}. The team ID is {team.id}. Share this ID with your friends who can join your team using this ID.'
            send_mail(
                'Team Details',
                message,
                'iitj.iotwebportal@gmail.com',
                [request.user.email],
                fail_silently=False,
            )
            # form.save_m2m()
            # return redirect('team_created', team.pk)
            return redirect(f'/events/{event.type}/{event.pk}')
    else:
        form = TeamCreationForm()
        return render(request, 'create_team.html', {'form': form, 'event':event})

@login_required
def join_team(request):
    if request.method == 'POST':
        form = TeamJoiningForm(request.POST)
        if form.is_valid():
            teamId = form.cleaned_data['teamId']
            if(Team.objects.filter(pk=teamId).exists()):
                team = Team.objects.get(pk=teamId)
                if request.user in team.members.all():
                    form.add_error(None, 'You are already a member of this team')
                elif team.event in request.user.events.all():
                    form.add_error(None, 'You have already registered for the event ' + team.event.name + ' from a different team')
                elif (team.members.all().count() >= team.event.max_team_size):
                    form.add_error(None, 'Team is already full')
                else:
                    response = redirect('join_team_confirm')
                    response['Location'] += '?id=' + teamId
                    return response
                    
            else:
                form.add_error('teamId', 'No team with the given team ID exists')
            # form.save_m2m()
            
    else:
        form = TeamJoiningForm()
    return render(request, 'join_team.html', {'form': form})
