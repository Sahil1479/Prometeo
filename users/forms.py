from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from allauth.account.forms import LoginForm
from .models import Team
CustomUser = get_user_model()


class SignUpForm(UserCreationForm):
    # password1 = forms.CharField(help_text="", required=True, label="Password")
    # password2 = forms.CharField(help_text="", required=True, label="Confirm Password")
    first_name = forms.CharField(help_text="", required=True)
    last_name = forms.CharField(help_text="", required=True)
    email = forms.EmailField(help_text="", required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = 'Email'
        # self.fields['login'].placeholder = 'Compulsory'


class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']


class TeamJoiningForm(forms.Form):
    teamId = forms.CharField(label="Team ID", max_length=9, min_length=9)


class EditTeamForm(forms.ModelForm):

    # members = forms.ModelMultipleChoiceField(CustomUser.objects.all(), required=False)

    class Meta:
        model = Team
        fields = ['name', 'members']

    def __init__(self, team, *args, **kwargs):
        super(EditTeamForm, self).__init__(*args, **kwargs)
        self.fields['members'].queryset = team.members.all()
