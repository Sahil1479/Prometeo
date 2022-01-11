from django import forms
# from django.forms.widgets import CheckboxSelectMultiple
# from django.contrib.auth.forms import UserCreatioznForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, get_user_model
from allauth.account.forms import LoginForm
CustomUser = get_user_model()
# from allauth.account.forms import SignupForm as NormalSignupForm, LoginForm
# import uuid
# from allauth.socialaccount.forms import SignupForm as SocialSignupForm
# from django.core.mail import send_mail
# from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    # username = None
    # first_name = forms.TextInput(attr={'type': 'text',
    #                                     'autofocus': 'autofocus',
    #                                     'class': 'form-control'
    #                                     })
    # last_name = forms.TextInput(attr={'type': 'text',
    #                                    'autofocus': 'autofocus',
    #                                    'class': 'form-control'
    #                                    })
    # email = forms.EmailField(attr={'type': 'email',
    #                                 'autofocus': 'autofocus',
    #                                 'class': 'form-control'
    #                                 })
    password1 = forms.CharField(help_text="", required=True, label="Password")
    password2 = forms.CharField(help_text="", required=True, label="Confirm Password")
    first_name = forms.CharField(help_text="", required=True)
    last_name = forms.CharField(help_text="", required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = 'Email'
        # self.fields['login'].placeholder = 'Compulsory'

