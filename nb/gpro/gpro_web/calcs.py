import math
from gpro.gpro_web.module.seleniumscrap import *
from gpro.gpro_web.module.track import trackdata
from gpro.gpro_web.module.partwear import partwear_lvl_factor


class Driver:
    def __init__(self):
        self.driver_stats = scrap.scrap_driver(scrapper)
        self.driver_dict_create()

    def driver_dict_create(self):
        i = self.driver_stats
        self.skill_dict = {'oa': i[0], 'con': i[1], 'tal': i[2], 'agg': i[3], 
        'exp': i[4], 'ti': i[5], 'sta': i[6], 'cha': i[7], 'mot': i[8], 
        'rep': i[9], 'wei': i[10], 'age': i[11] }

class Car:
    def __init__(self):
        self.car_stats = scrap.scrap_car(scrapper)
        self.car_dict_create()

    def car_dict_create(self):
        i = self.car_stats
        self.car_dict = {'cha': i['Nadwozie'], 'eng': i['Silnik'], 
        'fw': i['Przednie skrzydło'], 'rw': i['Tylne skrzydło'],
        'und': i['Podwozie'], 'sid': i['Wloty powietrza'], 'coo': i['Chłodzenie']
        ,'gea': i['Skrzynia biegów'],'bra': i['Hamulce'],'sus': i['Zawieszenie'],
        'ele': i['Elektronika']}
        

class Weather:
    def __init__(self):
        self.weather_data = scrap.scrap_weather(scrapper)
        self.q1 = self.weather_data['q1']
        self.q2 = self.weather_data['q2']
        self.race = self.weather_race_add_to_data()

    def weather_race_add_to_data(self):
        self.weather_data['race'] = {
            'weather': calcs.gpro_race_weather,
            'temp': int(calcs.gpro_race_temp),
            'hum': int(calcs.gpro_race_hum),
        }
        return self.weather_data['race']

class Track:
    def __init__(self, weather):
        self.name = weather.weather_data['track']
        self.data = trackdata[self.name]

class Tyre:
    def __init__(self):
        self.tyre_dict = {'durability': scrap.scrap_tyre(scrapper)}

class Calcs:
    def __init__(self):
        self.risk = 59
        self.data_confirm = False
        self.setup_car_factor_multipliers_dict()
        self.setup_driver_factor_multipliers_dict()
        self.setup_weather_factor_multipliers_dict()

    def setup_car_factor_wings_multipliers_dict(self):
        return {'fw': (30.03, -0.59), 'rw': (30.03, -0.59),
                     'cha': (-19.74, 0.47), 'und': (-15.07, 0.32)}


    def setup_car_factor_engine_multipliers_dict(self):
        return {'eng': (16.04, -0.51), 'coo': (4.9, -0.09),
                     'ele': (3.34, -0.04)}

    def setup_car_factor_brakes_multipliers_dict(self):
        return {'cha': (6.04, -0.14), 'bra': (-29.14, 0.71),
                     'ele': (6.11, -0.09)}

    def setup_car_factor_gearbox_multipliers_dict(self):
        return {'gea': (-41, 1.09), 'ele': (9, -0.14)}

    def setup_car_factor_suspension_multipliers_dict(self):
        return {'cha': (-15.27, 0.34), 'und': (-10.72, 0.23),
                     'sus': (31, -0.7), 'sid': (6.03, -0.12)}

    def setup_car_factor_multipliers_dict(self):
        self.setup_mult_dict = {
            'wings': self.setup_car_factor_wings_multipliers_dict(),
            'eng': self.setup_car_factor_engine_multipliers_dict(),
            'bra': self.setup_car_factor_brakes_multipliers_dict(),
            'gea': self.setup_car_factor_gearbox_multipliers_dict(),
            'sus': self.setup_car_factor_suspension_multipliers_dict(),  
        }

    def setup_driver_factor_multipliers_dict(self):
        self.setup_driver_factors_dict = {
                     'wings': {'tal': -0.246534498671854},
                     'eng': {'agg': 0.29521804804429},
                     'bra': {'tal': -0.498},
                     'gea': {'con': 0.5},
                     'sus': {'wei': 2, 'exp': 0.75},
                     }

    def setup_weather_factor_multipliers_dict(self):
        self.setup_weather_fact_dict = {
            'wings': {'dry': 12, 'wet': 263},
            'eng': {'dry': -3, 'wet': (0.7, -190)},
            'bra': {'dry': 6, 'wet': (3.9883754414027, 105.532592432347)},
            'gea': {'dry': -4, 'wet': (8.01996418151657, - 4.74271170354302)},
            'sus': {'dry': -6, 'wet': (-1, -257)},
            'ws': {'dry': 0.376337780506523, 'wet': 0.376337780506523},
        }
    
    def setup_weather_factor(self, weather, mode, weather_mode):
        self.weather_mode(weather, weather_mode)
        if weather.mode == 'wet':
            if mode == 'wings':
                return (weather.mode['temp'] 
                        * self.setup_weather_fact_dict[mode]['wet'] * 2)
            return (weather.mode['temp'] 
                    * self.setup_weather_fact_dict[mode]['wet'][0]
                    + self.setup_weather_fact_dict[mode]['wet'][1])
        return weather.mode['temp'] * self.setup_weather_fact_dict[mode]['dry']
            
        
    def weather_mode(self, weather, mode):
        if mode == "q2":
            weather.mode = weather.q2
        elif mode == 'race':
            weather.mode = weather.race
        else:
            weather.mode = weather.q1

    def setup_driver_factor(self, driver, mode):
        driver_factor = 0 
        for skill, mult in self.setup_driver_factors_dict[mode].items():
            driver_factor += driver.skill_dict[skill] * mult
        return driver_factor

    def setup_car_factor(self, car, mode):
        car_lvl_factor, car_wear_factor = 0, 0
        for part in self.setup_mult_dict[mode]:
            car_lvl_factor += (
            car.car_dict[part]['lvl'] * self.setup_mult_dict[mode][part][0]
            )
            car_wear_factor += (
            car.car_dict[part]['wear'] * self.setup_mult_dict[mode][part][1]
            )
        return car_lvl_factor, car_wear_factor
        

    def wings_calc_driver_factor(self, driver, base, weather_factor):
        driver_factor = driver.skill_dict['tal'] * math.floor((base
        + weather_factor)) * -0.001349079032746
        return driver_factor

    def wings_calc(self, track, weather, driver, car, mode=''):
        base = track.data['wings'] * 2
        car_lvl_factor, car_wear_factor = self.setup_car_factor(car, 'wings')
        weather_factor = self.setup_weather_factor(weather, 'wings', mode)
        driver_factor = self.wings_calc_driver_factor(driver, base, weather_factor)
        return (base + weather_factor + (driver_factor
            + car_lvl_factor) + car_wear_factor)/2

    def ws_calc_factors(self, car, driver, weather, mode, track):
        ws_wing_factor = ((car.car_dict['fw']['lvl'] + car.car_dict['rw']['lvl'])/2 
        * 3.69107049712848)
        driver_factor = self.setup_driver_factor(driver, 'wings')
        ws_weather_factor = self.setup_weather_factor(weather, 'ws', mode)
        ws_setup_factor = (self.wings_calc(track, weather, driver, car
        ,mode) * -0.189968386659174)
        return ws_wing_factor, driver_factor, ws_weather_factor, ws_setup_factor

    def ws_calc(self, track, weather, driver, car, mode=''):
        ws_calc_factors = self.ws_calc_factors(car, driver, weather, mode, track)
        ws = (track.data['ws']+ ws_calc_factors[1]
            + ws_calc_factors[0] + ws_calc_factors[2] + ws_calc_factors[3])
        if weather.mode['weather'] == 'dry':
            return ws
        return ws + 58.8818967363256

    def setup_calc_all_factors(self, weather, driver, car, mode, part):
        driver_factor = self.setup_driver_factor(driver, part)
        car_lvl_factor, car_wear_factor = self.setup_car_factor(car, part)
        car_factor = car_lvl_factor + car_wear_factor
        weather_factor = self.setup_weather_factor(weather, part, mode)
        return (driver_factor + car_factor + weather_factor, weather_factor)

    def eng_calc(self, track, weather, driver, car, mode=''):
        factors = self.setup_calc_all_factors(weather, driver, car, mode, 'eng')
        base_factor = (track.data['eng_set'] + factors[1]) * 0.001655723 + 0.0469416263186552
        return (track.data['eng_set'] + base_factor * driver.skill_dict['exp'] + factors[0])


    def bra_calc(self, track, weather, driver, car, mode=''):
        factors = self.setup_calc_all_factors(weather, driver, car, mode, 'bra')
        return track.data['bra'] + factors[0]

    def gea_calc(self, track, weather, driver, car, mode=''):
        factors = self.setup_calc_all_factors(weather, driver, car, mode, 'gea')
        return track.data['gea'] + factors[0]

    def sus_calc(self, track, weather, driver, car, mode=''):
        factors = self.setup_calc_all_factors(weather, driver, car, mode, 'sus')
        return track.data['sus'] + factors[0]


    def fuel_factors_calc(self, driver, car, weather):
        self.fuel_factors_dict = {
            'driver': [
                {'con': 1.00008, 'agg': 1.00018,'exp': 1.00014,'ti': 1.00036},
                driver.skill_dict ],
            'car': [{'eng': 1.014, 'ele': 1.009}, car.car_dict],
            'weather': [{'hum': 1.00025}, weather.race],
        }
        self.fuel_factors = 0

    def fuel_calc_factors(self,track):
        for el in self.fuel_factors_dict.keys():
            mode = self.fuel_factors_dict[el][1]
            for fctr, mt in self.fuel_factors_dict[el][0].items():
                mf = mode[fctr]['lvl'] if el == 'car' else mode[fctr]
                to_add = (track.data['fuel'] - track.data['fuel']
                * ( mt ** (mf - track.data[fctr])))
                self.fuel_factors += -(to_add) if fctr == 'agg' else to_add

    def fuel_calc(self, track, weather, driver, car):
        self.fuel_factors_calc(driver, car, weather)
        self.fuel_calc_factors(track)
        track_fuel = (self.fuel_factors + track.data['fuel']) * 1.01
        return track_fuel, track_fuel * (track.data['wc']/100 + 0.01)

    def tyre_calc(self, track, weather, driver, car, tyre):
        self.tyre_calc_mults(track)
        self.tyre_factors_calc(driver, car, weather, track, tyre)
        self.tyre_calc_factors()
        self.tyre_calc_comp_wear(track)
        return self.tyre_wear_list


    def tyre_calc_mults(self, track):
        self.tyre_comp_mults = [[0, 0.998163750229071], [1, 0.997064844817654],
        [2, 0.996380346554349], [3, 0.995862526048112], [5, 0.996087854384523]]
        self.tyre_other_mults = [129.776458172062, 0.73]
        self.track_base = self.tyre_other_mults[0] * track.data['ctrack2']
        self.wet_track_base = self.track_base * self.tyre_other_mults[1]


    def tyre_calc_factors(self):
        for el in self.tyre_factors_dict.keys():
            mode = self.tyre_factors_dict[el][1]
            for fctr, mt in self.tyre_factors_dict[el][0].items():
                mf = mode[fctr]['lvl'] if el == 'car' else mode[fctr]
                to_mult = mt ** mf 
                self.tyre_factors = self.tyre_factors * to_mult


   
    def tyre_factors_calc(self, driver, car, weather, track, tyre):
        self.tyre_factors_dict = {
            'driver': [
                {'agg': 0.999670155,'exp': 1.00022936,'wei': 0.999858329},
                driver.skill_dict ],
            'car': [{'sus': 1.009339294}, car.car_dict],
            'weather': [{'temp': 0.988463622}, weather.race],
            'track': [{'tyre_wear': 0.896416176238624}, track.data],
            'tyre': [{'durability': 1.048876356}, tyre.tyre_dict],
        }
        self.tyre_factors = 1

    def tyre_calc_comp_wear(self, track):
        self.tyre_wear_list = list()
        for comp in self.tyre_comp_mults:
            tyre_comp_factor = 1.390293715 ** comp[0]
            risk_factor = comp[1] ** self.risk
            mult = (self.tyre_factors * tyre_comp_factor * risk_factor)
            base = self.wet_track_base if comp[0] == 5 else self.track_base
            self.tyre_wear_list.append(mult * base)
    

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

    def part_wear(self, track, driver, car):
        driv_factor = self.part_wear_driv_factor(driver)
        part_wear = dict()
        for part in car.car_dict.keys():
            part_wear[part] = self.part_wear_calc(track, car, driv_factor, part)
        return part_wear