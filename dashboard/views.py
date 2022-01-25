from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from users.models import ExtendedUser, Team
from events.models import Event
import xlsxwriter
import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from .forms import EmailForm
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
sendMailID = settings.EMAIL_HOST_USER


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/events/')
def update_event_state(request, type, eventid, redirect_url_name):
    updated_event = get_object_or_404(Event, pk=eventid)
    updated_event.event_started = not updated_event.event_started
    updated_event.save()
    return HttpResponseRedirect(reverse(redirect_url_name))


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/users/')
def users_info(request):
    users = ExtendedUser.objects.all()
    wbname = 'Campus Ambassador List.xlsx'
    wbpath = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', wbname))
    workbook = xlsxwriter.Workbook(wbpath)
    ca_list = ExtendedUser.objects.filter(ambassador=True)
    worksheet = workbook.add_worksheet('CA List')
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
        'bg_color': 'gray',
        'font_size': 20
    })
    header_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': 'white',
        'bg_color': 'black'
    })
    # invalid_format = workbook.add_format({
    #     'bg_color': '#ff7f7f',
    #     'align': 'center',
    #     'valign': 'vcenter',
    # })
    # light_format = workbook.add_format({
    #     'bg_color': '#d3d3d3',
    #     'align': 'center',
    #     'valign': 'vcenter',
    # })

    worksheet.merge_range('A1:E1', 'Campus Ambassadors', merge_format)
    worksheet.write(1, 0, "Email", header_format)
    worksheet.write(1, 1, "Name", header_format)
    worksheet.write(1, 2, "Referral Id", header_format)
    worksheet.write(1, 3, "Contact", header_format)
    worksheet.write(1, 4, "College", header_format)
    row = 2

    for ca in ca_list:
        worksheet.write(row, 0, ca.user.email)
        worksheet.write(row, 1, ca.first_name + ' ' + ca.last_name)
        worksheet.write(row, 2, ca.invite_referral)
        worksheet.write(row, 3, ca.contact)
        worksheet.write(row, 4, ca.college)
        row += 1
    workbook.close()
    return render(request, 'dashboard/users_info.html', {'users': users, 'wbname': wbname})


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/users/')
def user_info(request, userid):
    user = get_object_or_404(ExtendedUser, pk=userid)
    teams = {}
    for team in user.teams.all():
        teams[team.event.pk] = team.name
    return render(request, 'dashboard/user_info.html', {'cur_user': user, 'teams': teams})


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/events/')
def events_info(request):
    events = Event.objects.all()
    return render(request, 'dashboard/events_info.html', {'events': events})


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/events/')
def event_type_info(request, type):
    events = Event.objects.filter(type=type).all()
    wbname = f'Events ({type}) Participation List.xlsx'
    wbpath = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', wbname))
    workbook = xlsxwriter.Workbook(wbpath)
    print(workbook)
    for event in events:
        participants = ExtendedUser.objects.filter(events=event)
        participating_teams = Team.objects.filter(event=event)
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
            'bg_color': 'gray',
            'font_size': 20
        })
        header_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'white',
            'bg_color': 'black'
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
            worksheet.merge_range('A1:H1', event.name + ' - Participants', merge_format)
            worksheet.write(1, 0, "Email", header_format)
            worksheet.write(1, 1, "First Name", header_format)
            worksheet.write(1, 2, "Last Name", header_format)
            worksheet.write(1, 3, "Contact", header_format)
            worksheet.write(1, 4, "Current Year", header_format)
            worksheet.write(1, 5, "College", header_format)
            worksheet.write(1, 6, "City", header_format)
            worksheet.write(1, 7, "Gender", header_format)
            row = 2
            for participant in participants:
                worksheet.write(row, 0, participant.user.email)
                worksheet.write(row, 1, participant.first_name)
                worksheet.write(row, 2, participant.last_name)
                worksheet.write(row, 3, participant.contact)
                worksheet.write(row, 4, participant.current_year.replace("_", " ").capitalize())
                worksheet.write(row, 5, participant.college)
                worksheet.write(row, 6, participant.city)
                worksheet.write(row, 7, participant.gender.capitalize())
                if(row % 2):
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
            for team in participating_teams:
                if(row % 2):
                    worksheet.set_row(row, cell_format=light_format)
                worksheet.write(row, 0, team.pk)
                worksheet.write(row, 1, team.name)
                i = 2
                for member in team.members.all():
                    worksheet.write(row, i, member.first_name + ' ' + member.last_name + f' ({member.user.email}, {member.contact})')
                    i = i + 1
                worksheet.write(row, event.max_team_size+2, team.leader.first_name + team.leader.last_name + f' ({team.leader.user.email})')
                if (team.members.all().count() < event.min_team_size or team.members.all().count() > event.max_team_size):
                    worksheet.write(row, event.max_team_size+3, "INELIGIBLE")
                    worksheet.set_row(row, cell_format=invalid_format)
                else:
                    worksheet.write(row, event.max_team_size+3, "ELIGIBLE")
                row = row + 1
    workbook.close()
    return render(request, 'dashboard/event_type_info.html', {'events': events, 'type': type, 'wbname': wbname})


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/events/')
def event_info(request, type, eventid):
    event = get_object_or_404(Event, pk=eventid)
    wbname = f'{event.name} Participation List.xlsx'
    wbpath = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', wbname))
    workbook = xlsxwriter.Workbook(wbpath)
    print(workbook)
    print(wbpath)
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
        'bg_color': 'gray',
        'font_size': 20
    })
    header_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': 'white',
        'bg_color': 'black'
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
        worksheet.merge_range('A1:H1', event.name + ' - Participants', merge_format)
        worksheet.write(1, 0, "Email", header_format)
        worksheet.write(1, 1, "First Name", header_format)
        worksheet.write(1, 2, "Last Name", header_format)
        worksheet.write(1, 3, "Contact", header_format)
        worksheet.write(1, 4, "Current Year", header_format)
        worksheet.write(1, 5, "College", header_format)
        worksheet.write(1, 6, "City", header_format)
        worksheet.write(1, 7, "Gender", header_format)
        row = 2
        for participant in event.participants.all():
            worksheet.write(row, 0, participant.user.email)
            worksheet.write(row, 1, participant.first_name)
            worksheet.write(row, 2, participant.last_name)
            worksheet.write(row, 3, participant.contact)
            worksheet.write(row, 4, participant.current_year.replace("_", " ").capitalize())
            worksheet.write(row, 5, participant.college)
            worksheet.write(row, 6, participant.city)
            worksheet.write(row, 7, participant.gender.capitalize())
            if(row % 2):
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
            if(row % 2):
                worksheet.set_row(row, cell_format=light_format)
            worksheet.write(row, 0, team.pk)
            worksheet.write(row, 1, team.name)
            i = 2
            for member in team.members.all():
                worksheet.write(row, i, f' ({member.user.email}, {member.contact})')
                i = i + 1
            worksheet.write(row, event.max_team_size+2, f'{team.leader.first_name} {team.leader.last_name}' + f' ({team.leader.user.email})')
            if (team.members.all().count() < event.min_team_size or team.members.all().count() > event.max_team_size):
                worksheet.write(row, event.max_team_size+3, "INELIGIBLE")
                worksheet.set_row(row, cell_format=invalid_format)
            else:
                worksheet.write(row, event.max_team_size+3, "ELIGIBLE")
            row = row + 1
    workbook.close()
    return render(request, 'dashboard/event_info.html', {'event': event, 'wbname': wbname})


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/?next=/dashboard/mass_mail/')
def mass_mail(request):
    # technical = Event.objects.filter(type='technical')
    # informal = Event.objects.filter(type='informal')
    # workshop = Event.objects.filter(type='workshop')
    # events = Event.objects.all()
    if (request.method == 'POST'):
        form = EmailForm(request.POST, request.FILES)
        if(form.is_valid()):
            recepients = ['garg.10@iitj.ac.in']   # add your required mail
            bcc = []
            iitj = request.POST.get('iitj')
            for event in form.cleaned_data['events']:
                users = ExtendedUser.objects.all()
                print(event)
                for participant in users:
                    print(participant.events.all())
                    if event in participant.events.all():
                        if(participant.user.email not in recepients):
                            if iitj:
                                bcc.append(participant.user.email)
                            else:
                                if 'iitj.ac.in' not in participant.user.email:
                                    bcc.append(participant.user.email)

            sender = sendMailID
            email = EmailMultiAlternatives(form.cleaned_data['subject'], form.cleaned_data['message'], sender, recepients, bcc=bcc)
            for file in request.FILES.getlist('attachments'):
                email.attach(file.name, file.read(), file.content_type)
            print(recepients)
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
    return render(request, 'dashboard/mass_mail.html', {'form': form})


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
