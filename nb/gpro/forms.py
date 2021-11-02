from django import forms
from django.forms.widgets import PasswordInput

class GPROForm(forms.Form):
    gpro_login = forms.CharField(widget=forms.TextInput(attrs={'class': "input", "width": "300px"}))
    gpro_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "input"}))
    gpro_risk = forms.CharField(widget=forms.NumberInput(attrs={'class': "input"}))
    gpro_race_weather = forms.CharField(widget=forms.TextInput(attrs={'class': "input"}))
    gpro_race_temp = forms.CharField(widget=forms.NumberInput(attrs={'class': "input"}))
    gpro_race_hum = forms.CharField(widget=forms.NumberInput(attrs={'class': "input"}))

class ScrapConfirmForm(forms.Form):
    confirm_if_values_look_correct = forms.CharField(widget=forms.TextInput(attrs={'class': "input", "width": "300px"}))