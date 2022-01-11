from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from allauth.account.forms import LoginForm
CustomUser = get_user_model()


class SignUpForm(UserCreationForm):
    # password1 = forms.CharField(help_text="", required=True, label="Password")
    # password2 = forms.CharField(help_text="", required=True, label="Confirm Password")
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
