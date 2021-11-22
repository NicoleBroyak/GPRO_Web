import math
from gpro.gpro_web.module.seleniumscrap import *
from gpro.gpro_web.module.track import trackdata
from gpro.gpro_web.module.partwear import partwear_lvl_factor
from django import apps, setup
from gpro.models import Calc_Data, Track, Season, Race
from nb.gpro import models

class Driver:
    def __init__(self):
        self.driver_stats = scrap.scrap_driver()
        self.driver_dict_create()

    def driver_dict_create(self):
        """Creates dictionary of driver attributes"""

        i = self.driver_stats
        self.skill_dict = {'oa': i[0], 'con': i[1], 'tal': i[2], 'agg': i[3], 
        'exp': i[4], 'ti': i[5], 'sta': i[6], 'cha': i[7], 'mot': i[8], 
        'rep': i[9], 'wei': i[10], 'age': i[11] }

class Car:

    def __init__(self):
        self.car_stats = scrap.scrap_car()
        self.car_dict_create()
        

    def car_dict_create(self):
        """Creates dictionary of car parts and their level and wear"""

        i = self.car_stats
        self.car_dict = {'cha': i['Nadwozie'], 'eng': i['Silnik'], 
        'fw': i['Przednie skrzydło'], 'rw': i['Tylne skrzydło'],
        'und': i['Podwozie'], 'sid': i['Wloty powietrza'], 'coo': i['Chłodzenie']
        ,'gea': i['Skrzynia biegów'],'bra': i['Hamulce'],'sus': i['Zawieszenie'],
        'ele': i['Elektronika']}
        
class Weather:
    """Class containing everything what is related to GPRO Weather"""

    def __init__(self):
        self.weather_data = scrap.scrap_weather()
        self.q1 = self.weather_data['q1']
        self.q2 = self.weather_data['q2']
        self.race = self.weather_race_add_to_data()

    def weather_race_add_to_data(self):
        """Creates dictionary of race weather and adds it to weather_data dict"""

        self.weather_data['race'] = {
            'weather': calcs.gpro_race_weather,
            'temp': float(calcs.gpro_race_temp),
            'hum': float(calcs.gpro_race_hum),
        }
        return self.weather_data['race']

class Track:
    """Class containing everything what is related to GPRO Tracks"""

    def __init__(self, weather):
        self.name = weather.weather_data['track']
        self.data = trackdata[self.name]

class Tyre:
    """Class containing everything what is related to GPRO Tyres"""


    def __init__(self):
        self.tyre_dict = {'durability': scrap.scrap_tyre()}


class Calcs:


    def __init__(self):
        self.risk = 0
        self.data_confirm = False

    def setup_car_factor_wings_multipliers_dict(self):
        """Returns dictionary of multipliers used in wings setup calculations"""

        return {'fw': (30.03, -0.59), 'rw': (30.03, -0.59),
                     'cha': (-19.74, 0.47), 'und': (-15.07, 0.32)}

    def setup_car_factor_engine_multipliers_dict(self):
        """Returns dictionary of multipliers used in engine setup calculations"""

        return {'eng': (16.04, -0.51), 'coo': (4.9, -0.09),
                     'ele': (3.34, -0.04)}

    def setup_car_factor_brakes_multipliers_dict(self):
        """Returns dictionary of multipliers used in brakes setup calculations"""

        return {'cha': (6.04, -0.14), 'bra': (-29.14, 0.71),
                     'ele': (6.11, -0.09)}

    def setup_car_factor_gearbox_multipliers_dict(self):
        """Returns dictionary of multipliers used in gearbox setup calculations"""

        return {'gea': (-41, 1.09), 'ele': (9, -0.14)}

    def setup_car_factor_suspension_multipliers_dict(self):
        """Returns dictionary of multipliers used in suspension setup calculations"""

        return {'cha': (-15.27, 0.34), 'und': (-10.72, 0.23),
                     'sus': (31, -0.7), 'sid': (6.03, -0.12)}

    def setup_car_factors_dict(self):
        """Returns dictionary of car multipliers used in setup calculations"""

        return {
            'wings': self.setup_car_factor_wings_multipliers_dict(),
            'eng': self.setup_car_factor_engine_multipliers_dict(),
            'bra': self.setup_car_factor_brakes_multipliers_dict(),
            'gea': self.setup_car_factor_gearbox_multipliers_dict(),
            'sus': self.setup_car_factor_suspension_multipliers_dict(),  
        }

    def setup_driver_factors_dict(self):
        """Returns dictionary of driver multipliers used in setup calculations"""
  
        return {
            'wings': {'tal': -0.246534498671854},
            'eng': {'agg': 0.29521804804429},
            'bra': {'tal': -0.498},
            'gea': {'con': 0.5},
            'sus': {'wei': 2, 'exp': 0.75},
        }

    def setup_weather_factor_dict(self):
        """Returns dictionary of weather multipliers used in setup calculations"""

        return {
            'wings': {'dry': 12, 'wet': 263},
            'eng': {'dry': -3, 'wet': (0.7, -190)},
            'bra': {'dry': 6, 'wet': (3.9883754414027, 105.532592432347)},
            'gea': {'dry': -4, 'wet': (8.01996418151657, - 4.74271170354302)},
            'sus': {'dry': -6, 'wet': (-1, -257)},
            'ws': {'dry': 0.376337780506523, 'wet': 0.376337780506523},
        }
    
    def setup_weather_factor(self, weather, setup_part, weather_mode):
        """Returns result of calculating weather factors:
        setup_part = name of setup part (wings, eng, bra, gea, sus)
        weather_mode = q1, q2 or race
        """
        
        self.weather_mode(weather, weather_mode)
        s, w, d = setup_part, weather.mode, self.setup_weather_factor_dict()[setup_part]
        r = (
            w['temp'] * d['wet'] * 2,
            w['temp'] * d['wet'][0] + d['wet'][1],
            w['temp'] * d['dry']
        )
        
        return r[2] if w == 'dry' else r[0] if s == 'wings' else r[1]
            
        
    def weather_mode(self, weather, mode):
        """Assigns weather mode with values of q1, q2 or race"""
       
        (m, w) = (mode, weather)
        w.mode = w.q2 if m == 'q2' else w.race if m == 'race' else w.q1


    def setup_driver_factor(self, driver, track, weather, mode, setup_part):
        """Returns results of calculating driver factors"""

        (d, t, w, m, s) = (driver, track, weather, mode, setup_part)
        if s != 'wings':
            dict = self.setup_driver_factors_dict()[s]
            return sum([d.skill_dict[sk] * mt for sk, mt in dict.items()])
        base = t.data['wings'] * 2
        wf = self.setup_weather_factor(w, 'wings', m)
        return d.skill_dict['tal'] * math.floor((base+ wf)) * -0.001349079032746

    def setup_car_factor(self, car, car_part):
        """Returns results of calculating car factors"""

        dict = self.setup_car_factors_dict()
        car_lvl_factor, car_wear_factor = 0, 0
        for part in dict[car_part]:
            car_lvl_factor += (
            car.car_dict[part]['lvl'] * dict[car_part][part][0]
            )
            car_wear_factor += (
            car.car_dict[part]['wear'] * dict[car_part][part][1]
            )
        return car_lvl_factor, car_wear_factor

    def setup_calc_all_factors(self, weather, driver, car, track, weather_mode, setup_part):
        """ Returns all calculated setup factors
        setup_part = name of setup part (wings, eng, bra, gea, sus)
        weather_mode = q1, q2 or race
        """

        driver_factor = self.setup_driver_factor(driver, track, weather, weather_mode, setup_part)
        car_lvl_factor, car_wear_factor = self.setup_car_factor(car, setup_part)
        car_factor = car_lvl_factor + car_wear_factor
        weather_factor = self.setup_weather_factor(weather, setup_part, weather_mode)
        return (driver_factor + car_factor + weather_factor, weather_factor)

    def setup_calc(self, track, weather, driver, car, weather_mode, setup_part):
        """Returns calculated setup for specified part
        setup_part = name of setup part (wings, eng, bra, gea, sus)
        weather_mode = q1, q2 or race
        """

        f = self.setup_calc_all_factors(weather, driver, car, track, weather_mode, setup_part)
        if setup_part not in ('eng', 'wings'):
            return track.data[setup_part] + f[0]
        elif setup_part != 'wings':
            f_2 = (track.data['eng_set'] + f[1]) * 0.001655723 + 0.0469416263186552
            return (track.data['eng_set'] + f_2 * driver.skill_dict['exp'] + f[0])
        return track.data[setup_part] + f[0]/2

    def ws_calc_factors(self, car, driver, weather, mode, wing_setup):
        """Returns results of calculating wing split factors"""

        ws_wing_factor = ((car.car_dict['fw']['lvl'] + car.car_dict['rw']['lvl'])/2 
        * 3.69107049712848)
        driver_factor = self.setup_driver_factor(driver, 'wings')
        ws_weather_factor = self.setup_weather_factor(weather, 'ws', mode)
        ws_setup_factor = wing_setup * -0.189968386659174
        return ws_wing_factor, driver_factor, ws_weather_factor, ws_setup_factor

    def ws_calc(self, track, weather, driver, car, mode, wing_setup):
        """Returns results of calculating wing split factors"""

        ws_calc_factors = self.ws_calc_factors(car, driver, weather, mode, wing_setup)
        ws = (track.data['ws']+ ws_calc_factors[1]
            + ws_calc_factors[0] + ws_calc_factors[2] + ws_calc_factors[3])
        if weather.mode['weather'] == 'dry':
            return ws
        return ws + 58.8818967363256
        
    def fuel_factors_dict(self, driver, car, weather):
        """Returns dictionary of fuel factors used in calculations"""

        return {
            'driver': [
                {'con': 1.00008, 'agg': 1.00018,'exp': 1.00014,'ti': 1.00036},
                driver.skill_dict ],
            'car': [{'eng': 1.014, 'ele': 1.009}, car.car_dict],
            'weather': [{'hum': 1.00025}, weather.race],
        }

    def fuel_calc_factors(self, track, driver, car, weather):
        """Calculates fuel factors"""

        d, factors = self.fuel_factors_dict(self, driver, car, weather), 0
        for el in d.keys():
            mode = d[el][1]
            for fctr, mult in d[el][0].items():
                mode_fctr = mode[fctr]['lvl'] if el == 'car' else mode[fctr]
                to_add = (track.data['fuel'] - track.data['fuel']
                * ( mult ** (mode_fctr - track.data[fctr])))
                factors += -(to_add) if fctr == 'agg' else to_add
        return factors

    def fuel_calc(self, track, weather, driver, car):
        """Calculates and returns fuel tuple (dry, wet)"""
        
        f = self.fuel_calc_factors(track, driver, car, weather)
        track_fuel = (f + track.data['fuel']) * 1.01
        return (track_fuel, track_fuel * (track.data['wc']/100 + 0.01))

    def create_fuel_wear_tuple(self, track, weather, driver, car):
        """Creates tuple of rounded fuel values:
        0: dry; 1: dry per lap; 2: wet; 3: wet per lap
        """
        
        fuel = self.fuel_calc(track, weather, driver, car)
        fuel_tuple = (
            round(fuel[0], 2), 
            round(fuel[0]/track.data['laps'],2),
            round(fuel[1], 2), 
            round(fuel[1]/track.data['laps'],2),
        )
        return fuel_tuple

    def tyre_calc(self, track, weather, driver, car, tyre):
        self.create_tyre_factors_mults(track)
        self.create_tyre_factors_dict(driver, car, weather, track, tyre)
        self.tyre_calc_factors()
        return self.tyre_calc_comp_wear(track)


    def create_tyre_factors_mults(self, track):
        self.tyre_comp_mults = [[0, 0.998163750229071], [1, 0.997064844817654],
        [2, 0.996380346554349], [3, 0.995862526048112], [5, 0.996087854384523]]
        self.tyre_other_mults = [129.776458172062, 0.73]
        self.track_base = self.tyre_other_mults[0] * track.data['ctrack2']
        self.wet_track_base = self.track_base * self.tyre_other_mults[1]


   
    def create_tyre_factors_dict(self, driver, car, weather, track, tyre):
        return {
            'driver': [
                {'agg': 0.999670155,'exp': 1.00022936,'wei': 0.999858329},
                driver.skill_dict ],
            'car': [{'sus': 1.009339294}, car.car_dict],
            'weather': [{'temp': 0.988463622}, weather.race],
            'track': [{'tyre_wear': 0.896416176238624}, track.data],
            'tyre': [{'durability': 1.048876356}, tyre.tyre_dict],
        }

    def tyre_calc_factors(self):
        for el in self.tyre_factors_dict.keys():
            mode = self.tyre_factors_dict[el][1]
            for fctr, mt in self.tyre_factors_dict[el][0].items():
                mf = mode[fctr]['lvl'] if el == 'car' else mode[fctr]
                to_mult = mt ** mf 
                self.tyre_factors = self.tyre_factors * to_mult

    def tyre_calc_comp_wear(self, track):
        tyre_wear_list = list()
        for comp in self.tyre_comp_mults:
            tyre_comp_factor = 1.390293715 ** comp[0]
            risk_factor = comp[1] ** self.risk
            mult = (self.tyre_factors * tyre_comp_factor * risk_factor)
            base = self.wet_track_base if comp[0] == 5 else self.track_base
            tyre_wear_list.append(mult * base)
        return tyre_wear_list
    
    def create_tyre_wear_list(self, track):
        self.tyre_calc(self.track, self.weather, self.driver, self.car, self.tyre)
        tyre_wear_list_100  = list()
        for tyre in self.tyre_wear_list:
            tyre_wear_list_100.append(math.floor(tyre / track.data['length']))
        tyre_wear_list_80 = list()
        for tyre in self.tyre_wear_list:
            tyre_wear_list_80.append(math.floor(tyre / track.data['length'] * 0.8))
        return tyre_wear_list_100, tyre_wear_list_80

    def part_wear_driv_factor(self, driver):
        con_factor = 0.998789138 ** driver.skill_dict['con']
        tal_factor = 0.998751839 ** driver.skill_dict['tal']
        exp_factor = 0.998707677 ** driver.skill_dict['exp']
        return exp_factor * con_factor * tal_factor


    def part_wear_calc(self, track, car, driv_factor, part):
        risk_factor = partwear_lvl_factor[car.car_dict[part]['lvl']] ** self.risk
        part_wear = driv_factor * risk_factor * track.data[part + '_wear']
        after_race = round(part_wear + car.car_dict[part]['wear'])
        return (round(part_wear), after_race)

    def part_wear_dict_create(self, track, driver, car):
        driv_factor = self.part_wear_driv_factor(driver)
        self.part_wear = dict()
        for part in car.car_dict.keys():
            self.part_wear[part] = self.part_wear_calc(track, car, driv_factor, part)
        self.part_wear

    def settings_calcs_to_list(self, track, weather, driver, car, weather_mode):
        wing_setup = self.setup_calc(track, weather, driver, car, weather_mode, 'wings')
        wing_split = self.ws_calc(track, weather, driver, car, weather_mode, wing_setup)
        settings = {
            'fw': round(wing_setup + wing_split),
            'rw': round(wing_setup - wing_split),
            'eng': round(self.setup_calc(track, weather, driver, car, weather_mode, 'eng')),
            'bra': round(self.setup_calc(track, weather, driver, car, weather_mode, 'bra')),
            'gea': round(self.setup_calc(track, weather, driver, car, weather_mode, 'gea')),
            'sus': round(self.setup_calc(track, weather, driver, car, weather_mode, 'sus')),
        }
        return settings

    def settings_dict_create(self, track, weather, driver, car):
        self.settings = dict()
        self.settings['q1'] = self.settings_calcs_to_list(track, weather, driver, car, 'q1')
        self.settings['q2'] = self.settings_calcs_to_list(track, weather, driver, car, 'q2')
        self.settings['race'] = self.settings_calcs_to_list(track, weather, driver, car, 'race')
        print(self.settings)
        for v in self.settings.values():
            print(v)

    def get_form_data(self, form):
        self.gpro_login = form.cleaned_data['gpro_login']
        self.gpro_password = form.cleaned_data['gpro_password']
        self.risk = form.cleaned_data['gpro_risk']
        self.gpro_race_weather = form.cleaned_data['gpro_race_weather']
        self.gpro_race_temp = form.cleaned_data['gpro_race_temp']
        self.gpro_race_hum = form.cleaned_data['gpro_race_hum']

    def create_settings_for_view(self, track, weather, driver, car):
        self.settings_dict_create(track, weather, driver, car)
        self.create_fuel_wear_tuple(track)
        self.create_tyre_wear_list(track)
        self.part_wear_dict_create(track, driver, car)

    def create_sub_objects(self):
        self.driver = Driver()
        self.weather = Weather()
        self.car = Car()
        self.track = Track(self.weather)
        self.tyre = Tyre()

    def create_database_entry(self, driver, weather, car):
        season = apps.apps.get_model('gpro', 'Season')
        track = apps.apps.get_model('gpro', 'Track')
        race = apps.apps.get_model('gpro', 'Race')
        season = season.objects.get(name=scrap.scrap_season_no())
        track_name = track.objects.get(name=self.track.name)
        d = Calc_Data(
        track = track_name,
        season = season,
        dri_oa = driver.skill_dict['oa'],
        dri_con = driver.skill_dict['con'],
        dri_tal = driver.skill_dict['tal'],
        dri_agg = driver.skill_dict['agg'],
        dri_exp = driver.skill_dict['exp'],
        dri_ti = driver.skill_dict['ti'],
        dri_sta = driver.skill_dict['sta'],
        dri_cha = driver.skill_dict['cha'],
        dri_mot = driver.skill_dict['mot'],
        dri_rep = driver.skill_dict['rep'],
        dri_wei = driver.skill_dict['wei'],
        dri_age = driver.skill_dict['age'],
        car_cha_lvl = car.car_dict['cha']['lvl'],
        car_cha_wear = car.car_dict['cha']['wear'],
        car_eng_lvl = car.car_dict['eng']['lvl'],
        car_eng_wear = car.car_dict['eng']['wear'],
        car_fw_lvl = car.car_dict['fw']['lvl'],
        car_fw_wear = car.car_dict['fw']['wear'],
        car_rw_lvl = car.car_dict['rw']['lvl'],
        car_rw_wear = car.car_dict['rw']['wear'],
        car_und_lvl = car.car_dict['und']['lvl'],
        car_und_wear = car.car_dict['und']['wear'],
        car_sid_lvl = car.car_dict['sid']['lvl'],
        car_sid_wear = car.car_dict['sid']['wear'],
        car_coo_lvl = car.car_dict['coo']['lvl'],
        car_coo_wear = car.car_dict['coo']['wear'],
        car_gea_lvl = car.car_dict['gea']['lvl'],
        car_gea_wear = car.car_dict['gea']['wear'],
        car_bra_lvl = car.car_dict['bra']['lvl'],
        car_bra_wear = car.car_dict['bra']['wear'],
        car_sus_lvl = car.car_dict['sus']['lvl'],
        car_sus_wear = car.car_dict['sus']['wear'],
        car_ele_lvl = car.car_dict['ele']['lvl'],
        car_ele_wear = car.car_dict['ele']['wear'],
        xs_wear = self.tyre_wear_list[0],
        s_wear = self.tyre_wear_list[1],
        m_wear = self.tyre_wear_list[2],
        h_wear = self.tyre_wear_list[3],
        r_wear = self.tyre_wear_list[4],
        fuel_dry_wear = self.fuel[0],
        fuel_wet_wear = self.fuel[1],
        risk = self.risk,
        temp = weather.race['temp'],
        hum = weather.race['hum'],
        )
        d.save()