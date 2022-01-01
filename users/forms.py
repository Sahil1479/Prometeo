from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
CustomUser = get_user_model()
# from allauth.account.forms import SignupForm as NormalSignupForm, LoginForm
# import uuid
# from allauth.socialaccount.forms import SignupForm as SocialSignupForm
# from django.core.mail import send_mail
# from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    # username = None
    # first_name = forms.CharField(max_length=100, required=True)
    # last_name = forms.CharField(max_length=100, required=True)
    # email = forms.EmailField(max_length=254, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email','first_name','last_name')