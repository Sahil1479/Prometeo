from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from allauth.account.forms import LoginForm
from .models import Team
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
CustomUser = get_user_model()


class SignUpForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
                attrs={
                        'data-theme': 'light',  # default=light
                        'data-size': 'normal',  # default=normal
                },
            ), )
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

    # def save(self, request):
    #     clientKey = request.POST.get('g-recaptcha-response')
    #     secretKey = settings.RECAPTCHA_PRIVATE_KEY

    #     captchaData = {
    #         'response': clientKey,
    #         'secret': secretKey
    #     }
    #     r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=captchaData)
    #     response = json.loads(r.text)
    #     verify = response['success']
    #     if verify is True:
    #         user = super(SignUpForm, self).save(request)
    #         return user
    #     else:

    #         raise forms.ValidationError("Invalid Captcha")


class CustomLoginForm(LoginForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
                attrs={
                        'data-theme': 'light',  # default=light
                        'data-size': 'normal',  # default=normal
                },
            ), )

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = 'Email'


class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']


class TeamJoiningForm(forms.Form):
    teamId = forms.CharField(label="Team ID", max_length=9, min_length=9)


class EditTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'members']

    def __init__(self, team, *args, **kwargs):
        super(EditTeamForm, self).__init__(*args, **kwargs)
        self.fields['members'].queryset = team.members.all()
