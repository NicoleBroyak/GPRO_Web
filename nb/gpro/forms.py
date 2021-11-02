from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.forms import UserCreationForm

class GPROForm(forms.Form):
    gpro_login = forms.CharField(widget=forms.TextInput())
    gpro_password = forms.CharField(widget=forms.PasswordInput())
    gpro_risk = forms.CharField(widget=forms.NumberInput())
    gpro_race_weather = forms.CharField(widget=forms.TextInput())
    gpro_race_temp = forms.CharField(widget=forms.NumberInput())
    gpro_race_hum = forms.CharField(widget=forms.NumberInput())

class ScrapConfirmForm(forms.Form):
    confirm_if_values_look_correct = forms.CharField(widget=forms.TextInput())

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)