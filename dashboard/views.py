from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from users.models import CustomUser, ExtendedUser, Team
from events.models import Event
import xlsxwriter
import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from .forms import EmailForm
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
# Create your views here.
sendMailID = settings.EMAIL_HOST_USER

current_year_dict = {'1': '1st Year', '2': '2nd Year', '3': '3rd Year', '4': '4th Year', '5': '5th Year',
                     '6': 'Graduated', '7': 'Faculty/Staff', '8': 'NA'}


def get_referred(email):
    users = ExtendedUser.objects.all()
    count = 0
    for user in users:
        print(user.referred_by)
        if user.referred_by is None:
            pass
        elif user.referred_by.email == email:
            count += 1
    return count


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/?next=/dashboard/events/')
def update_event_state(request, type, eventid, redirect_url_name):
    updated_event = get_object_or_404(Event, pk=eventid)
    updated_event.event_started = not updated_event.event_started
    updated_event.save()
    return HttpResponseRedirect(reverse(redirect_url_name))


def get_ca_export(filename):
    wbname = filename
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
    row = 2
    worksheet.merge_range('A1:F1', 'Campus Ambassadors', merge_format)
    worksheet.write(1, 0, "Email", header_format)
    worksheet.write(1, 1, "Name", header_format)
    worksheet.write(1, 2, "Referral Id", header_format)
    worksheet.write(1, 3, "Contact", header_format)
    worksheet.write(1, 4, "College", header_format)
    worksheet.write(1, 5, "No of referred users", header_format)
    for ca in ca_list:
        if 'iitj' not in ca.college.lower() and 'iit jodhpur' not in ca.college.lower() and 'indian institute of technology jodhpur' not in ca.college.lower() and 'indian institute of technology, jodhpur' not in ca.college.lower():
            worksheet.write(row, 0, ca.user.email)
            worksheet.write(row, 1, ca.first_name + ' ' + ca.last_name)
            worksheet.write(row, 2, ca.invite_referral)
            worksheet.write(row, 3, ca.contact)
            worksheet.write(row, 4, ca.college)
            worksheet.write(row, 5, get_referred(ca.user.email))
            print(get_referred(ca.user.email))
            row += 1
    workbook.close()


def get_all_user_export(filename):
    users = ExtendedUser.objects.all()
    wbname2 = filename
    wbpath2 = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', wbname2))
    workbook2 = xlsxwriter.Workbook(wbpath2)
    worksheet2 = workbook2.add_worksheet('Users List')
    col_center2 = workbook2.add_format({
        'align': 'center',
        'valign': 'vcenter',
    })
    worksheet2.set_column(0, 100, 30, col_center2)
    worksheet2.set_row(0, 30)
    merge_format2 = workbook2.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': 'gray',
        'font_size': 20
    })
    header_format2 = workbook2.add_format({
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
    worksheet2.merge_range('A1:G1', 'User List', merge_format2)
    worksheet2.write(1, 0, "Email", header_format2)
    worksheet2.write(1, 1, "Name", header_format2)
    worksheet2.write(1, 2, "Contact", header_format2)
    worksheet2.write(1, 3, "Referred By", header_format2)
    worksheet2.write(1, 4, "Campus Ambassador", header_format2)
    worksheet2.write(1, 5, "College", header_format2)
    worksheet2.write(1, 6, "Current Year", header_format2)
    row2 = 2

    for user in users:
        worksheet2.write(row2, 0, user.user.email)
        worksheet2.write(row2, 1, user.first_name + ' ' + user.last_name)
        worksheet2.write(row2, 2, user.contact)
        worksheet2.write(row2, 3, str(user.referred_by)) if user.referred_by is not None else worksheet2.write(row2, 3, 'NA')
        worksheet2.write(row2, 4, 'YES') if user.ambassador else worksheet2.write(row2, 4, 'NO')
        worksheet2.write(row2, 5, user.college)
        worksheet2.write(row2, 6, current_year_dict[user.current_year])
        row2 += 1
    workbook2.close()


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/?next=/dashboard/users/')
def downloadfile(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', filename))
    if filename == "User_List":
        get_all_user_export(filename + '.xlsx')
    elif filename == "Campus_Ambassador_List":
        get_ca_export(filename + '.xlsx')
    file_path += '.xlsx'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/?next=/dashboard/users/')
def users_info(request):
    users = ExtendedUser.objects.all()
    wbname = 'User_List'
    wbname2 = 'Campus_Ambassador_List'
    return render(request, 'dashboard/users_info.html', {'users': users, 'wbname': wbname, 'wbname2': wbname2})


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/?next=/dashboard/users/')
def user_info(request, userid):
    user = get_object_or_404(CustomUser, pk=userid)
    teams = {}
    for team in user.teams.all():
        teams[team.event.pk] = team.name
    return render(request, 'dashboard/user_info.html', {'cur_user': user, 'teams': teams})


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/?next=/dashboard/events/')
def events_info(request):
    events = Event.objects.all()
    return render(request, 'dashboard/events_info.html', {'events': events})


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/?next=/dashboard/events/')
def event_type_info(request, type):
    events = Event.objects.filter(type=type).all()
    wbname = f'Events ({type}) Participation List.xlsx'
    wbpath = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', wbname))
    workbook = xlsxwriter.Workbook(wbpath)
    wbname2 = f'Events ({type}) Eligible Participants List.xlsx'
    wbpath2 = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', wbname2))
    workbook2 = xlsxwriter.Workbook(wbpath2)
    for event in events:
        participants = ExtendedUser.objects.filter(events=event)
        participating_teams = Team.objects.filter(event=event)
        if(len(event.name) > 31):
            worksheet = workbook.add_worksheet(event.name[:31])
            worksheet2 = workbook2.add_worksheet(event.name[:31])
        else:
            worksheet = workbook.add_worksheet(event.name)
            worksheet2 = workbook2.add_worksheet(event.name)
        col_center = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
        })
        col_center2 = workbook2.add_format({
            'align': 'center',
            'valign': 'vcenter',
        })
        worksheet.set_column(0, 100, 30, col_center)
        worksheet.set_row(0, 30)
        worksheet2.set_column(0, 100, 30, col_center2)
        worksheet2.set_row(0, 30)
        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': 'gray',
            'font_size': 20
        })
        merge_format2 = workbook2.add_format({
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
        header_format2 = workbook2.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'white',
            'bg_color': 'black'
        })
        light_format = workbook.add_format({
            'bg_color': '#d3d3d3',
            'align': 'center',
            'valign': 'vcenter',
        })
        light_format2 = workbook2.add_format({
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
                worksheet.write(row, 4, current_year_dict[participant.current_year].capitalize())
                worksheet.write(row, 5, participant.college)
                worksheet.write(row, 6, participant.city)
                worksheet.write(row, 7, participant.gender.capitalize())
                if(row % 2):
                    worksheet.set_row(row, cell_format=light_format)
                row = row + 1
        else:
            worksheet.merge_range('A1:' + str(chr(event.max_team_size+68))+'1', event.name + ' - Participanting Teams', merge_format)
            worksheet2.merge_range('A1:' + str(chr(event.max_team_size+68))+'1', event.name + ' - Participanting Teams', merge_format2)
            worksheet.write(1, 0, "Team ID", header_format)
            worksheet2.write(1, 0, "Team ID", header_format2)
            worksheet.write(1, 1, "Team Name", header_format)
            worksheet2.write(1, 1, "Team Name", header_format2)
            for i in range(1, event.max_team_size+1):
                worksheet.write(1, i+1, "Member " + str(i), header_format)
                worksheet2.write(1, i+1, "Member " + str(i), header_format2)
            worksheet.write(1, event.max_team_size+2, "Created By", header_format)
            worksheet2.write(1, event.max_team_size+2, "Created By", header_format2)
            worksheet.write(1, event.max_team_size+3, "Status", header_format)
            worksheet2.write(1, event.max_team_size+3, "Status", header_format2)
            row = 2
            row2 = 2
            for team in participating_teams:
                if(row % 2):
                    worksheet.set_row(row, cell_format=light_format)
                    worksheet2.set_row(row2, cell_format=light_format2)
                worksheet.write(row, 0, team.pk)
                worksheet.write(row, 1, team.name)
                i = 2
                for member in team.members.all():
                    worksheet.write(row, i, member.extendeduser.first_name + ' ' + member.extendeduser.last_name + f' ({member.email}, {member.extendeduser.contact})')
                    i = i + 1
                worksheet.write(row, event.max_team_size+2, team.leader.first_name + team.leader.last_name + f' ({team.leader.email})')
                if (team.members.all().count() < event.min_team_size or team.members.all().count() > event.max_team_size):
                    worksheet.write(row, event.max_team_size+3, "INELIGIBLE")
                    worksheet.set_row(row, cell_format=invalid_format)
                else:
                    worksheet.write(row, event.max_team_size+3, "ELIGIBLE")
                    worksheet2.write(row2, 0, team.pk)
                    worksheet2.write(row2, 1, team.name)
                    i2 = 2
                    for member in team.members.all():
                        worksheet2.write(row2, i2, member.extendeduser.first_name + ' ' + member.extendeduser.last_name + f' ({member.email}, {member.extendeduser.contact})')
                        i2 = i2 + 1
                    worksheet2.write(row2, event.max_team_size+2, team.leader.first_name + team.leader.last_name + f' ({team.leader.email})')
                    worksheet2.write(row2, event.max_team_size+3, "ELIGIBLE")
                    row2 += 1
                row = row + 1
    workbook.close()
    workbook2.close()
    return render(request, 'dashboard/event_type_info.html', {'events': events, 'type': type, 'wbname': wbname, 'wbname2': wbname2})


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/?next=/dashboard/events/')
def event_info(request, type, eventid):
    event = get_object_or_404(Event, pk=eventid)
    wbname = f'{event.name} Participation List.xlsx'
    wbpath = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', wbname))
    workbook = xlsxwriter.Workbook(wbpath)
    wbname2 = f'{event.name} Eligible Participants List.xlsx'
    wbpath2 = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', wbname2))
    workbook2 = xlsxwriter.Workbook(wbpath2)
    if(len(event.name) > 31):
        worksheet = workbook.add_worksheet(event.name[:31])
        worksheet2 = workbook2.add_worksheet(event.name[:31])
    else:
        worksheet = workbook.add_worksheet(event.name)
        worksheet2 = workbook2.add_worksheet(event.name)
    col_center = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
    })
    col_center2 = workbook2.add_format({
        'align': 'center',
        'valign': 'vcenter',
    })
    worksheet.set_column(0, 100, 30, col_center)
    worksheet.set_row(0, 30)
    worksheet2.set_column(0, 100, 30, col_center2)
    worksheet2.set_row(0, 30)
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': 'gray',
        'font_size': 20
    })
    merge_format2 = workbook2.add_format({
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
    header_format2 = workbook2.add_format({
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
    light_format2 = workbook2.add_format({
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
            worksheet.write(row, 4, current_year_dict[participant.current_year].capitalize())
            worksheet.write(row, 5, participant.college)
            worksheet.write(row, 6, participant.city)
            worksheet.write(row, 7, participant.gender.capitalize())
            if(row % 2):
                worksheet.set_row(row, cell_format=light_format)
            row = row + 1
    else:
        worksheet.merge_range('A1:' + str(chr(event.max_team_size+68))+'1', event.name + ' - Participanting Teams', merge_format)
        worksheet.write(1, 0, "Team ID", header_format)
        worksheet.write(1, 1, "Team Name", header_format)
        worksheet2.merge_range('A1:' + str(chr(event.max_team_size+68))+'1', event.name + ' - Participanting Teams', merge_format2)
        worksheet2.write(1, 0, "Team ID", header_format2)
        worksheet2.write(1, 1, "Team Name", header_format2)
        for i in range(1, event.max_team_size+1):
            worksheet.write(1, i+1, "Member " + str(i), header_format)
            worksheet2.write(1, i+1, "Member " + str(i), header_format2)
        worksheet.write(1, event.max_team_size+2, "Created By", header_format)
        worksheet.write(1, event.max_team_size+3, "Status", header_format)
        worksheet2.write(1, event.max_team_size+2, "Created By", header_format2)
        worksheet2.write(1, event.max_team_size+3, "Status", header_format2)
        row = 2
        row2 = 2
        for team in event.participating_teams.all():
            if(row % 2):
                worksheet.set_row(row, cell_format=light_format)
                worksheet2.set_row(row2, cell_format=light_format2)
            worksheet.write(row, 0, team.pk)
            worksheet.write(row, 1, team.name)
            i = 2
            for member in team.members.all():
                worksheet.write(row, i, f' ({member.email}, {member.extendeduser.contact})')
                i = i + 1
            worksheet.write(row, event.max_team_size+2, f'{team.leader.first_name} {team.leader.last_name}' + f' ({team.leader.email})')
            if (team.members.all().count() < event.min_team_size or team.members.all().count() > event.max_team_size):
                worksheet.write(row, event.max_team_size+3, "INELIGIBLE")
                worksheet.set_row(row, cell_format=invalid_format)
            else:
                worksheet.write(row, event.max_team_size+3, "ELIGIBLE")
                worksheet2.write(row2, event.max_team_size+3, "ELIGIBLE")
                worksheet2.write(row2, 0, team.pk)
                worksheet2.write(row2, 1, team.name)
                i2 = 2
                for member in team.members.all():
                    worksheet2.write(row2, i2, f' ({member.email}, {member.extendeduser.contact})')
                    i2 = i2 + 1
                worksheet2.write(row2, event.max_team_size+2, f'{team.leader.first_name} {team.leader.last_name}' + f' ({team.leader.email})')
                row2 = row2 + 1
            row = row + 1
    workbook.close()
    workbook2.close()
    return render(request, 'dashboard/event_info.html', {'event': event, 'wbname': wbname, 'wbname2': wbname2})


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/?next=/dashboard/mass_mail/')
def mass_mail(request):
    # technical = Event.objects.filter(type='technical')
    # informal = Event.objects.filter(type='informal')
    # workshop = Event.objects.filter(type='workshop')
    # events = Event.objects.all()
    if (request.method == 'POST'):
        form = EmailForm(request.POST, request.FILES)
        if(form.is_valid()):
            recepients = [settings.EVENTS_MAIL_RECEPIENTS]   # add your required mail
            bcc = []
            iitj = request.POST.get('iitj')
            for event in form.cleaned_data['events']:
                users = ExtendedUser.objects.all()
                for participant in users:
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


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/?next=/dashboard/events/')
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
