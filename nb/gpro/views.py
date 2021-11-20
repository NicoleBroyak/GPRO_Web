from django.db import models
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, context, RequestContext
from gpro.gpro_web import calcs as c
from gpro.gpro_web.module import seleniumscrap as s
from django.urls import reverse
from django.contrib.auth import login
from gpro.models import Season as season_model
import math

from gpro.forms import GPROForm, ScrapConfirmForm, CustomUserCreationForm

def home(request):
    return render(request, 'gpro/index.html')

def gprocalc1(request):
    c.calcs = c.Calcs()
    form = GPROForm(request.POST)
    if form.is_valid():
        c.calcs.get_form_data(form)
        return HttpResponseRedirect('/gpro_main')

    return render(request, 'gpro/gprocalc1.html', {'form': form})

def gpro_main(request):
    
    calcs = c.calcs
    form = ScrapConfirmForm(request.POST)
    if not calcs.data_confirm:
        s.scrap.gpro_login(calcs.gpro_login, calcs.gpro_password)
        calcs.create_sub_objects()
        weather = calcs.weather
        context = {
        'weather': weather.weather_data,
        'form': form,
        'calcs': calcs,
    }
    if form.is_valid():
        calcs.data_confirm = True
        track, driver, car, tyre = calcs.track, calcs.driver, calcs.car, calcs.tyre
        calcs.create_settings_for_view(track, weather, driver, car)
        calcs.create_database_entry(driver, weather, car)
        s.scrap.reset_scrapper()
        context =  {
            'car': car,
            'car_dict': car.car_dict,
            'driver': driver,
            'driver_dict': driver.skill_dict,
            'weather': weather,
            'track': track,
            'tyre': tyre,
            'calcs': calcs,
            'partwear': calcs.part_wear,
            'setup': calcs.settings.values(),
        }
    return render(request, 'gpro/gpro_main.html', context=context)


def register(request):
    if request.method == "GET":
        return render(
            request, "gpro/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
