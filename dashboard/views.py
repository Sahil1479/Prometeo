from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from users.models import *
from events.models import *
import xlsxwriter
import os
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import *

# Create your views here.

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/users/')
def users_info(request):
    users = CustomUser.objects.all()
    return render(request, 'dashboard/users_info.html', {'users':users})

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/users/')
def user_info(request, userid):
    user = get_object_or_404(CustomUser, pk=userid)
    teams = {}
    for team in user.teams.all():
        teams[team.event.pk] = team.name
    return render(request, 'dashboard/user_info.html', {'cur_user':user, 'teams' : teams})

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/events/')
def events_info(request):
    events = Event.objects.all()
    return render(request, 'dashboard/events_info.html', {'events':events})

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/events/')
def event_type_info(request, type):
    events = Event.objects.filter(type=type).all()
    wbname = f'Events ({type}) Participation List.xlsx'
    wbpath = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', wbname))
    workbook = xlsxwriter.Workbook(wbpath)
    for event in events:
        if(len(event.name) > 31):
            worksheet = workbook.add_worksheet(event.name[:31])
        else:
            worksheet = workbook.add_worksheet(event.name)
        col_center = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
        })
        worksheet.set_column(0, 100, 30, col_center)
        worksheet.set_row(0, 30)
        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color' : 'gray',
            'font_size' : 20
        })
        header_format = workbook.add_format({
            'bold' : 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_color' : 'white',
            'bg_color' : 'black'
        }) 
        invalid_format = workbook.add_format({
            'bg_color': '#ff7f7f',
            'align': 'center',
            'valign': 'vcenter',
        })
        light_format = workbook.add_format({
            'bg_color': '#d3d3d3',
            'align': 'center',
            'valign': 'vcenter',
        })
        if (event.participation_type == 'individual'):
            worksheet.merge_range('A1:B1', event.name + ' - Participants', merge_format)
            worksheet.write(1, 0, "Username", header_format)
            worksheet.write(1, 1, "Email", header_format)
            worksheet.write(1, 2, "First Name", header_format)
            worksheet.write(1, 3, "Last Name", header_format)
            worksheet.write(1, 4, "Contact", header_format)
            worksheet.write(1, 5, "Current Year", header_format)
            worksheet.write(1, 6, "College", header_format)
            worksheet.write(1, 7, "City", header_format)
            worksheet.write(1, 8, "Gender", header_format)
            row = 2
            for participant in event.participants.all():
                worksheet.write(row, 0, participant.username)
                worksheet.write(row, 1, participant.email)
                worksheet.write(row, 2, participant.first_name)
                worksheet.write(row, 3, participant.last_name)
                worksheet.write(row, 4, participant.contact)
                worksheet.write(row, 5, participant.current_year.replace("_", " ").capitalize())
                worksheet.write(row, 6, participant.college)
                worksheet.write(row, 7, participant.city)
                worksheet.write(row, 8, participant.gender.capitalize())
                if(row%2):
                    worksheet.set_row(row, cell_format=light_format)
                row = row + 1
        else:
            worksheet.merge_range('A1:I1', event.name + ' - Participanting Teams', merge_format)
            worksheet.write(1, 0, "Team ID", header_format)
            worksheet.write(1, 1, "Team Name", header_format)
            for i in range(1, event.max_team_size+1):
                worksheet.write(1, i+1, "Member " + str(i), header_format)
            worksheet.write(1, event.max_team_size+2, "Created By", header_format)
            worksheet.write(1, event.max_team_size+3, "Status", header_format)
            row = 2
            for team in event.participating_teams.all():
                if(row%2):
                    worksheet.set_row(row, cell_format=light_format)
                worksheet.write(row, 0, team.pk)
                worksheet.write(row, 1, team.name)
                i = 2
                for member in team.members.all():
                    worksheet.write(row, i, member.username + f' ({member.email}, {member.contact})')
                    i = i + 1
                worksheet.write(row, event.max_team_size+2, team.leader.username + f' ({team.leader.email})')
                if (team.members.all().count() < event.min_team_size or team.members.all().count() > event.max_team_size):
                    worksheet.write(row, event.max_team_size+3, "INELIGIBLE")
                    worksheet.set_row(row, cell_format=invalid_format)
                else:
                    worksheet.write(row, event.max_team_size+3, "ELIGIBLE")
                row = row + 1
    workbook.close()
    return render(request, 'dashboard/event_type_info.html', {'events':events, 'type':type, 'wbname' : wbname})

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/events/')
def event_info(request, type, eventid):
    event = get_object_or_404(Event, pk=eventid)

    wbname = f'{event.name} Participation List.xlsx'
    wbpath = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', wbname))
    workbook = xlsxwriter.Workbook(wbpath)

    if(len(event.name) > 31):
        worksheet = workbook.add_worksheet(event.name[:31])
    else:
        worksheet = workbook.add_worksheet(event.name)
    col_center = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
    })
    worksheet.set_column(0, 100, 30, col_center)
    worksheet.set_row(0, 30)
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color' : 'gray',
        'font_size' : 20
    })
    header_format = workbook.add_format({
        'bold' : 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_color' : 'white',
        'bg_color' : 'black'
    }) 
    invalid_format = workbook.add_format({
        'bg_color': '#ff7f7f',
        'align': 'center',
        'valign': 'vcenter',
    })
    light_format = workbook.add_format({
        'bg_color': '#d3d3d3',
        'align': 'center',
        'valign': 'vcenter',
    })
    if (event.participation_type == 'individual'):
        worksheet.merge_range('A1:B1', event.name + ' - Participants', merge_format)
        worksheet.write(1, 0, "Username", header_format)
        worksheet.write(1, 1, "Email", header_format)
        worksheet.write(1, 2, "First Name", header_format)
        worksheet.write(1, 3, "Last Name", header_format)
        worksheet.write(1, 4, "Contact", header_format)
        worksheet.write(1, 5, "Current Year", header_format)
        worksheet.write(1, 6, "College", header_format)
        worksheet.write(1, 7, "City", header_format)
        worksheet.write(1, 8, "Gender", header_format)
        row = 2
        for participant in event.participants.all():
            worksheet.write(row, 0, participant.username)
            worksheet.write(row, 1, participant.email)
            worksheet.write(row, 2, participant.first_name)
            worksheet.write(row, 3, participant.last_name)
            worksheet.write(row, 4, participant.contact)
            worksheet.write(row, 5, participant.current_year.replace("_", " ").capitalize())
            worksheet.write(row, 6, participant.college)
            worksheet.write(row, 7, participant.city)
            worksheet.write(row, 8, participant.gender.capitalize())
            if(row%2):
                worksheet.set_row(row, cell_format=light_format)
            row = row + 1
    else:
        worksheet.merge_range('A1:I1', event.name + ' - Participanting Teams', merge_format)
        worksheet.write(1, 0, "Team ID", header_format)
        worksheet.write(1, 1, "Team Name", header_format)
        for i in range(1, event.max_team_size+1):
            worksheet.write(1, i+1, "Member " + str(i), header_format)
        worksheet.write(1, event.max_team_size+2, "Created By", header_format)
        worksheet.write(1, event.max_team_size+3, "Status", header_format)
        row = 2
        for team in event.participating_teams.all():
            if(row%2):
                worksheet.set_row(row, cell_format=light_format)
            worksheet.write(row, 0, team.pk)
            worksheet.write(row, 1, team.name)
            i = 2
            for member in team.members.all():
                worksheet.write(row, i, member.username + f' ({member.email}, {member.contact})')
                i = i + 1
            worksheet.write(row, event.max_team_size+2, team.leader.username + f' ({team.leader.email})')
            if (team.members.all().count() < event.min_team_size or team.members.all().count() > event.max_team_size):
                worksheet.write(row, event.max_team_size+3, "INELIGIBLE")
                worksheet.set_row(row, cell_format=invalid_format)
            else:
                worksheet.write(row, event.max_team_size+3, "ELIGIBLE")
            row = row + 1
    
    workbook.close()
    return render(request, 'dashboard/event_info.html', {'event':event, 'wbname':wbname})

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/mass_mail/')
def mass_mail(request):
    # technical = Event.objects.filter(type='technical')
    # informal = Event.objects.filter(type='informal')
    # workshop = Event.objects.filter(type='workshop')
    # events = Event.objects.all()
    if (request.method == 'POST'):
        form = EmailForm(request.POST, request.FILES)
        if(form.is_valid()):
            recepients = []
            iitj = request.POST.get('iitj')
            # print(iitj)
            for event in form.cleaned_data['events']:
                for participant in event.participants.all():
                    if(participant.email not in recepients):
                        if(iitj):
                            recepients.append(participant.email)
                        elif ('iitj.ac.in' not in participant.email):
                            recepients.append(participant.email)

            sender = ''
            if(form.cleaned_data['sender']):
                sender = form.cleaned_data['sender']
            else:
                sender = 'info.noreply@prometeo.in'
            
            email = EmailMessage(form.cleaned_data['subject'], form.cleaned_data['message'], sender, recepients)
            for file in request.FILES.getlist('attachments'):
                email.attach(file.name, file.read(), file.content_type)
            email.send()
            messages.success(request, "Mails sent!")
            return redirect('mass_mail')
        # recepients = []
        # for event in events:
        #     if(request.POST.get('check'+str(event.pk))):
        #         for participant in event.participants.all():
        #             if(participant.email not in recepients):
        #                 recepients.append(participant.email)
        # subject = request.POST.get('subject')
        # message = request.POST.get('message')
        # print(recepients)
        # send_mail(
        #     subject,
        #     message,
        #     "info.noreply@prometeo.in",
        #     recepients,
        #     fail_silently=False
        # )
        # messages.success(request, "Mails sent!")
        # return redirect('mass_mail')
    else:
        form = EmailForm()
    return render(request, 'dashboard/mass_mail.html', {'form':form})

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/events/')
def change_registration(request, type, eventid, value):
    event = get_object_or_404(Event, pk=eventid)
    if(value == 'open'):
        event.registration_open = True
        messages.success(request, 'Successfully opened registration for event ' + event.name + '.')
    else:
        event.registration_open = False
        messages.success(request, 'Successfully closed registration for event ' + event.name + '.')
    event.save()
    return redirect('event_info', type, eventid)