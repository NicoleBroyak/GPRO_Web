from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.forms import UserCreationForm

class GPROForm(forms.Form):
    gpro_login = forms.CharField(widget=forms.TextInput())
    gpro_password = forms.CharField(widget=forms.PasswordInput())
    gpro_risk = forms.IntegerField(widget=forms.NumberInput(attrs={'value': 50}))
    gpro_race_weather = forms.ChoiceField(choices=(('dry', 'dry'), ('wet', 'wet')))
    gpro_race_temp = forms.IntegerField(widget=forms.NumberInput(attrs={'value': 25}))
    gpro_race_hum = forms.IntegerField(widget=forms.NumberInput(attrs={'value': 50}))

class ScrapConfirmForm(forms.Form):
    confirm_if_values_look_correct = forms.CharField(widget=forms.TextInput())

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)