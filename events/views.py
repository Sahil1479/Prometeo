from django.shortcuts import render, redirect
from .models import Brochure, Event
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import date, datetime
from .models import EVENT_CHOICES, Panel
from users.models import CustomUser, Submissions
from django.conf import settings
import boto3


def registrationNotCompleted(request):
    user = request.user
    if user.is_authenticated and user.extendeduser.isProfileCompleted is False:
        messages.info(request, 'Complete your registration first.')
        return True
    return False


def events(request, type):
    if registrationNotCompleted(request):
        return redirect("/users/profile")

    events = Event.objects.all()
    today = date.today()
    brochure = Brochure.objects.filter(type=type).first()
    if type == 'live':
        liveevents = Event.objects.filter(end_date__gte=today).filter(date__lte=today).filter(event_started=True).filter(hidden=False).order_by('time')
        return render(request, 'liveevents.html', {'liveevents': liveevents, 'type': type,
                                                   'present_time': datetime.now(),
                                                   })
    elif type == 'talk':
        events = Event.objects.filter(type=type).filter(hidden=False).order_by('rank')
        return render(request, 'speakers.html', {'events': events, 'type': type, 'brochure': brochure, })
    elif type == 'panel_discussion':
        events = Event.objects.filter(type=type).filter(hidden=False).order_by('rank')
        panelist = Panel.objects.all()
        return render(request, 'panel.html', {'events': events, 'panelists': panelist, 'type': type})
    elif type == 'poster_presentation':
        events = Event.objects.filter(type=type).filter(hidden=False).order_by('rank')
        if events:
            submissions = Submissions.objects.filter(event=events.first().id)
        else:
            submissions = Submissions.objects.all()
        submitted_users = []
        for submission in submissions:
            submitted_users.append(submission.user)
        return render(request, 'poster_presentation.html', {'events': events,  'type': type, 'brochure': brochure, 'submittedUsers':submitted_users})
    else:
        typeFound = False
        for item in EVENT_CHOICES:
            if type == item[0]:
                typeFound = True
        if typeFound is False:
            messages.info(request, 'No event type exists with the given name.')
            return redirect("/")
        events = Event.objects.filter(type=type).filter(hidden=False).order_by('rank')
        return render(request, 'events.html', {'events': events, 'type': type, 'brochure': brochure, })


def event(request, type, eventid):
    if registrationNotCompleted(request):
        return redirect("/users/profile")
    event = get_object_or_404(Event, pk=eventid)
    return render(request, 'event.html', {'event': event})


def schedule(request):
    if registrationNotCompleted(request):
        return redirect("/users/profile")
    schedule_file = Brochure.objects.filter(type='schedule_file').first()
    day1 = Event.objects.filter(date="2022-02-26").order_by('time')
    day2 = Event.objects.filter(date="2022-02-27").order_by('time')
    day3 = Event.objects.filter(date="2022-02-28").order_by('time')
    day4 = Event.objects.filter(date="2022-03-01").order_by('time')
    return render(request, 'schedule.html', {'day1': day1, 'day2': day2, 'day3': day3, 'day4': day4, 'schedule_file': schedule_file, })

def uploadSubmission(request):
    if request.method == 'GET':
        return redirect('/events/poster_presentation')
    # POST
    try:
        user_email = request.user
        event_name = request.POST.get('event')
        fileUploaded = request.FILES.get('fileUploaded')
        print(fileUploaded)
        cloudFilename = str(event_name) + '/' + str(user_email) + '-' + fileUploaded.name 

        session = boto3.session.Session(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        s3 = session.resource('s3')
        s3.Bucket(settings.AWS_BUCKET).put_object(Key=cloudFilename, Body=fileUploaded)

        # saving in db
        submitted_user = CustomUser.objects.get(email__exact = user_email)
        submitted_to_event = Event.objects.get(name = event_name)
 
        file_url = "https://prometeo-bucket.s3.ap-south-1.amazonaws.com/" + cloudFilename

        Submissions.objects.create(user=submitted_user, event = submitted_to_event, file_url=file_url)

        messages.info(request, 'File Uploaded Succesfully!')
    
    except Exception as e:
        print(e)
        messages.info(request, 'There was an error submitting your file, Please try again')
    
    return redirect('/events/poster_presentation')