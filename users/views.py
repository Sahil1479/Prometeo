from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import ExtendedUser
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import uuid
from django.contrib import messages

User = get_user_model()

# Create your views here.


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


        # print("Hello World: ", isCampusAmbassador)
        # print("Hello World Referral: ", referralCode)

        extendeduser = ExtendedUser.objects.filter(user=request.user).first()

        # If the current user is using referral code.
        if referralCode and referralCode != "default":
            referredBy = ExtendedUser.objects.filter(invite_referral = referralCode).first()
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
        if extendeduser.ambassador == True:
            invite_referral = 'CA' + str(uuid.uuid4().int)[:6]
            extendeduser.invite_referral = invite_referral
            send_mail(
                'Campus Ambassador',
                f'Dear {user.first_name},\nYou have been enrolled as a campus ambassador. Your referral code for inviting others is {invite_referral}.\nRegards,\nPrometeo 2022 Team',
                'iitj.iotwebportal@gmail.com',
                [user.email],
                fail_silently=False,
            )

        extendeduser.isProfileCompleted = True
        extendeduser.save()
        messages.success(request, 'Your profile was updated.') 

    return render(request, 'profile.html')
