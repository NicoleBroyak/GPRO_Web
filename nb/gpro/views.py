from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, context, RequestContext
from gpro.gpro_web import calcs as c
from gpro.gpro_web.module import seleniumscrap as s
from django.urls import reverse
from django.contrib.auth import login
import math

from gpro.forms import GPROForm, ScrapConfirmForm, CustomUserCreationForm

def home(request):
    return render(request, 'gpro/index.html')

def gprocalc1(request):
    # create a form instance and populate it with data from the request:
    c.calcs = c.Calcs()
    form = GPROForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        c.calcs.gpro_login = form.cleaned_data['gpro_login']
        c.calcs.gpro_password = form.cleaned_data['gpro_password']
        c.calcs.risk = int(form.cleaned_data['gpro_risk'])
        c.calcs.gpro_race_weather = form.cleaned_data['gpro_race_weather']
        c.calcs.gpro_race_temp = form.cleaned_data['gpro_race_temp']
        c.calcs.gpro_race_hum = form.cleaned_data['gpro_race_hum']
        return HttpResponseRedirect('/gpro_main')

    return render(request, 'gpro/gprocalc1.html', {'form': form})

def gpro_main(request):
    
    calcs = c.calcs
    form = ScrapConfirmForm(request.POST)
    if not calcs.data_confirm:
        s.gpro_login(s.scrapper, calcs.gpro_login, calcs.gpro_password)
        weather = c.Weather()
        context = {
        'weather': weather.weather_data,
        'form': form,
        'calcs': calcs,
    }
    if form.is_valid():
        calcs.data_confirm = True
        calcs = c.calcs
        print(calcs.gpro_login)
        weather = c.Weather()
        track = c.Track(weather)
        driver = c.Driver()
        car = c.Car()
        tyre = c.Tyre()
        calcs.wing_split = calcs.ws_calc(track, weather, driver, car)
        calcs.wing_setup = calcs.wings_calc(track, weather, driver, car)
        calcs.eng = calcs.eng_calc(track, weather, driver, car)
        calcs.bra = calcs.bra_calc(track, weather, driver, car)
        calcs.gea = calcs.gea_calc(track, weather, driver, car)
        calcs.sus = calcs.sus_calc(track, weather, driver, car)
        calcs.wing_splitq2 = calcs.ws_calc(track, weather, driver, car, mode='q2')
        calcs.wing_setupq2 = calcs.wings_calc(track, weather, driver, car, mode='q2')
        calcs.engq2 = calcs.eng_calc(track, weather, driver, car, mode='q2')
        calcs.braq2 = calcs.bra_calc(track, weather, driver, car, mode='q2')
        calcs.geaq2 = calcs.gea_calc(track, weather, driver, car, mode='q2')
        calcs.susq2 = calcs.sus_calc(track, weather, driver, car, mode='q2')
        calcs.wing_splitr = calcs.ws_calc(track, weather, driver, car, mode='race')
        calcs.wing_setupr = calcs.wings_calc(track, weather, driver, car, mode='race')
        calcs.engr = calcs.eng_calc(track, weather, driver, car, mode='race')
        calcs.brar = calcs.bra_calc(track, weather, driver, car, mode='race')
        calcs.gear = calcs.gea_calc(track, weather, driver, car, mode='race')
        calcs.susr = calcs.sus_calc(track, weather, driver, car, mode='race')
        calcs.fuel = calcs.fuel_calc(track, weather, driver, car)
        calcs.tyre = calcs.tyre_calc(track, weather, driver, car, tyre)
        calcs.fw = calcs.wing_setup + calcs.wing_split
        calcs.rw = calcs.wing_setup - calcs.wing_split
        calcs.fwq2 = calcs.wing_setupq2 + calcs.wing_splitq2
        calcs.rwq2 = calcs.wing_setupq2 - calcs.wing_splitq2
        calcs.fwr = calcs.wing_setupr + calcs.wing_splitr
        calcs.rwr = calcs.wing_setupr - calcs.wing_splitr
        calcs.setup_list = {
            'fw': [round(calcs.fw), round(calcs.fwq2), round(calcs.fwr)],
            'rw': [round(calcs.rw), round(calcs.rwq2), round(calcs.rwr)],
            'eng': [round(calcs.eng), round(calcs.engq2), round(calcs.engr)],
            'bra': [round(calcs.bra), round(calcs.braq2), round(calcs.brar)],
            'gea': [round(calcs.gea), round(calcs.geaq2), round(calcs.gear)],
            'sus': [round(calcs.sus), round(calcs.susq2), round(calcs.susr)]
        }
        #print(f'tyre max distance: XS: {tyre[0]}'
        #      f'S: {tyre[1]}, M: {tyre[2]}, H: {tyre[3]}, R: {tyre[4]}')
        #print(fuel)
        calcs.fuel_wear_list = [
            round(calcs.fuel[0], 2),
            round(calcs.fuel[0]/track.laps,2),
            round(calcs.fuel[1], 2),
            round(calcs.fuel[1]/track.laps,2),
        ]
        calcs.tyre_wear_list = [
            math.floor(calcs.tyre[0]/track.length),
            math.floor(calcs.tyre[1]/track.length),
            math.floor(calcs.tyre[2]/track.length),
            math.floor(calcs.tyre[3]/track.length),
            math.floor(calcs.tyre[4]/track.length),
        ]
        calcs.tyre_wear_list_80 = [
            math.floor(math.prod([calcs.tyre[0], 0.8])/track.length),
            math.floor(math.prod([calcs.tyre[1], 0.8])/track.length),
            math.floor(math.prod([calcs.tyre[2], 0.8])/track.length),
            math.floor(math.prod([calcs.tyre[3], 0.8])/track.length),
            math.floor(math.prod([calcs.tyre[4], 0.8])/track.length),
        ]
        calcs.partwear = calcs.part_wear(track, driver, car)
        s.scrapper.quit()
        context =  {
            'car': car,
            'driver': driver,
            'weather': weather,
            'track': track,
            'tyre': tyre,
            'calcs': calcs,
            'partwear': calcs.partwear,
            'setup': calcs.setup_list,
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
