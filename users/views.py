from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ExtendedUser, Team
from events.models import Event
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import uuid
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import TeamCreationForm, TeamJoiningForm, EditTeamForm

User = get_user_model()


def isRegistrationFormValid(data):
    requiredFields = ['first_name', 'last_name', 'email', 'college_name', 'phone_no', 'gender', 'city', 'current_year']
    for item in requiredFields:
        if item not in data:
            return False
    return True


@login_required
def user_profile(request):
    if(request.method == "POST"):
        data = request.POST
        if isRegistrationFormValid(data):
            user = request.user
            user.first_name = data['first_name']
            user.last_name = data['last_name']

            extendeduser = ExtendedUser.objects.filter(user=request.user).first()
            extendeduser.gender = data['gender']
            extendeduser.contact = data['phone_no']
            extendeduser.current_year = data['gender']
            extendeduser.college = data['college_name']
            extendeduser.city = data['city']
            extendeduser.current_year = data['current_year']
            if 'referral_code' in data and data['referral_code'] != '' and extendeduser.isProfileCompleted is False:
                referralCode = data['referral_code']
                if ExtendedUser.objects.filter(invite_referral=referralCode).exists():
                    referredBy = ExtendedUser.objects.filter(invite_referral=referralCode).first()
                    extendeduser.referred_by = referredBy.user
                else:
                    messages.info(request, 'Invalid Referral Code.')
                    return render(request, 'profile.html')

            extendeduser.isProfileCompleted = True
            extendeduser.save()
            user.save()
            messages.info(request, 'Your profile has been updated.')
            return redirect('/')

        else:
            messages.info(request, 'Fill all the required fields.')

    return render(request, 'profile.html')


@login_required
def create_team(request, eventid):
    event = get_object_or_404(Event, pk=eventid)
    if(request.user.teams.filter(event=event).exists()):
        messages.info(request, 'You have already created a team for this event.')
        return redirect(f'/events/{event.type}/{event.pk}')
    if event.registration_open is False:
        messages.info(request, 'Registration for this event is currently closed.')
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
            message = (f'You have just created team "{team.name}" for the {event.type} event {event.name}. The team ID is {team.id}. Share this ID with your friends who can join your team using this ID.')
            send_mail(
                'Team Details',
                message,
                'iitj.iotwebportal@gmail.com',
                [request.user.email],
                fail_silently=False,
            )
            messages.info(request, f'Team Successfully Created, your teamId is {team.id}, which is also sent to your respective email address.')
            return redirect(f'/events/{event.type}/{event.pk}')
    else:
        form = TeamCreationForm()
        return render(request, 'create_team.html', {'form': form, 'event': event})


@login_required
def join_team(request):
    if request.method == 'POST':
        form = TeamJoiningForm(request.POST)
        if form.is_valid():
            teamId = form.cleaned_data['teamId']
            if(Team.objects.filter(pk=teamId).exists()):
                team = Team.objects.get(pk=teamId)
                if team.event.registration_open is False:
                    messages.info(request, 'Registration for this event is currently closed.')
                    return redirect(f'/events/{team.event.type}/{team.event.pk}')
                if request.user in team.members.all():
                    form.add_error(None, 'You are already a member of this team')
                elif team.event in request.user.extendeduser.events.all():
                    form.add_error(None, 'You have already registered for the event ' + team.event.name + ' from a different team')
                elif (team.members.all().count() >= team.event.max_team_size):
                    form.add_error(None, 'Team is already full')
                else:
                    team.members.add(request.user)
                    team.save()
                    request.user.extendeduser.events.add(team.event)
                    messages.success(request, f"Successfully joined team '{team.name}'.")
                    return redirect(f'/events/{team.event.type}/{team.event.pk}')

            else:
                form.add_error('teamId', 'No team with the given team ID exists')
    else:
        form = TeamJoiningForm()
    return render(request, 'join_team.html', {'form': form})


@login_required
def edit_team(request, teamid):
    team = get_object_or_404(Team, id=teamid)
    if(request.user != team.leader):
        messages.info(request, "Only the team leader (creator) can edit the team details.")
        return redirect(f'/events/{team.event.type}/{team.event.pk}')
    elif(request.method == 'POST'):
        form = EditTeamForm(team, request.POST, instance=team)
        if(form.is_valid()):
            if(team.leader not in form.cleaned_data['members']):
                form.add_error('members', 'You cannot remove the leader (creator) of the team from the team.')
            else:
                form.save()
                for member in team.members.all():
                    if member not in form.cleaned_data['members']:
                        member.extendeduser.events.remove(team.event)

                messages.success(request, "The team details have been updated.")
                return redirect((f'/events/{team.event.type}/{team.event.pk}'))
    else:
        form = EditTeamForm(team, instance=team)
    return render(request, 'edit_team.html', {'form': form, 'team': team})


@login_required
def delete_team(request, teamid):
    team = get_object_or_404(Team, id=teamid)
    if(request.user != team.leader):
        messages.info(request, "Only the team leader (creator) can delete the team.")
        return redirect(f'/events/{team.event.type}/{team.event.pk}')
    for member in team.members.all():
        member.extendeduser.events.remove(team.event)
    team.delete()
    messages.success(request, f"Successfully deleted team '{team.name}'.")
    return redirect(f'/events/{team.event.type}/{team.event.pk}')
