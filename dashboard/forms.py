from django import forms
from events.models import *

class EmailForm(forms.Form):
    events = forms.ModelMultipleChoiceField(Event.objects.all(), widget=forms.CheckboxSelectMultiple(), label="Events")
    subject = forms.CharField(max_length=100, label="Subject")
    message = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":40}), label="Message/Body")
    iitj = forms.BooleanField(label="Include IITJ emails", initial = True, required=False)
    attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}) ,label="Attach Files", required=False)