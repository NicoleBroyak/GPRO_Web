import math
from gpro.gpro_web.module.seleniumscrap import *
from gpro.gpro_web.module.track import trackdata
from gpro.gpro_web.module.partwear import partwear_lvl_factor


class Driver:
    def __init__(self):
        self.driver_stats = scrap_driver(scrapper)
        self.oa = self.driver_stats[0]
        self.con = self.driver_stats[1]
        self.tal = self.driver_stats[2]
        self.agg = self.driver_stats[3]
        self.exp = self.driver_stats[4]
        self.ti = self.driver_stats[5]
        self.sta = self.driver_stats[6]
        self.cha = self.driver_stats[7]
        self.mot = self.driver_stats[8]
        self.rep = self.driver_stats[9]
        self.wei = self.driver_stats[10]
        self.age = self.driver_stats[11]
        self.driver_dict_create()

    def driver_dict_create(self):
        self.skill_dict = {
            'oa': self.driver_stats[0],
            'con': self.driver_stats[1],
            'tal': self.driver_stats[2],
            'agg': self.driver_stats[3],
            'exp': self.driver_stats[4],
            'ti': self.driver_stats[5],
            'sta': self.driver_stats[6],
            'cha': self.driver_stats[7],
            'mot': self.driver_stats[8],
            'rep': self.driver_stats[9],
            'wei': self.driver_stats[10],
            'age': self.driver_stats[11],

        }

class Car:
    def __init__(self):
        self.car_stats = scrap_car(scrapper)
        self.cha = self.car_stats['Nadwozie']
        self.eng = self.car_stats['Silnik']
        self.fw = self.car_stats['Przednie skrzydło']
        self.rw = self.car_stats['Tylne skrzydło']
        self.und = self.car_stats['Podwozie']
        self.sid = self.car_stats['Wloty powietrza']
        self.coo = self.car_stats['Chłodzenie']
        self.gea = self.car_stats['Skrzynia biegów']
        self.bra = self.car_stats['Hamulce']
        self.sus = self.car_stats['Zawieszenie']
        self.ele = self.car_stats['Elektronika']
        self.car_dict_create()

# poprawić docelowo, żeby init nie dublował się
    def car_dict_create(self):
        self.car_dict = {
            'cha': self.car_stats['Nadwozie'],
            'eng': self.car_stats['Silnik'],
            'fw': self.car_stats['Przednie skrzydło'],
            'rw': self.car_stats['Tylne skrzydło'],
            'und': self.car_stats['Podwozie'],
            'sid': self.car_stats['Wloty powietrza'],
            'coo': self.car_stats['Chłodzenie'],
            'gea': self.car_stats['Skrzynia biegów'],
            'bra': self.car_stats['Hamulce'],
            'sus': self.car_stats['Zawieszenie'],
            'ele': self.car_stats['Elektronika'],

        }
        

class Weather:
    def __init__(self):
        self.weather_data = scrap_weather(scrapper)
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
        data = trackdata[self.name]
        self.data = trackdata[self.name]
        self.pow = data['power']
        self.han = data['handling']
        self.acc = data['acceleration']
        self.downforce = data['downforce']
        self.overtaking = data['overtaking']
        self.sus = data['suspension_track']
        self.corners = data['corners']
        self.length= data['length']
        self.laps = data['laps']
        self.tyre_wear = data['tyre_wear']
        self.fuel_wear = data['fuel_wear']
        self.ctrack = data['ctrack2_']
        self.ws = data['ws']
        self.wings = data['wings']
        self.eng = data['eng']
        self.bra = data['bra']
        self.gea = data['gea']
        self.sus = data['sus']
        self.fuel = data['fuel']
        self.con = data['con']
        self.agg = data['agg']
        self.exp = data['exp']
        self.ti = data['ti']
        self.englvl = data['eng']
        self.ele = data['ele']
        self.hum = data['hum']
        self.wc = data['wc']/100
        self.cha_wear = data['cha_wear']
        self.eng_wear = data['eng_wear']
        self.fw_wear = data['fw_wear']
        self.rw_wear = data['rw_wear']
        self.und_wear = data['und_wear']
        self.sid_wear = data['sid_wear']
        self.coo_wear = data['coo_wear']
        self.gea_wear = data['gea_wear']
        self.bra_wear = data['bra_wear']
        self.sus_wear = data['sus_wear']
        self.ele_wear = data['ele_wear']

class Tyre:
    def __init__(self):
        self.durability = scrap_tyre(scrapper)

class Calcs:
    def __init__(self):
        self.risk = 59
        self.data_confirm = False
        self.setup_car_factor_multipliers_dict()
        self.setup_driver_factor_multipliers_dict()
        self.setup_weather_factor_multipliers_dict()

    def setup_car_factor_wings_multipliers_dict(self):
        setup_dict = {
                     'fw': (30.03, -0.59),
                     'rw': (30.03, -0.59),
                     'cha': (-19.74, 0.47),
                     'und': (-15.07, 0.32),
                     }
        return setup_dict


    def setup_car_factor_engine_multipliers_dict(self):
        setup_dict = {
                     'eng': (16.04, -0.51),
                     'coo': (4.9, -0.09),
                     'ele': (3.34, -0.04),
                     }
        return setup_dict

    def setup_car_factor_brakes_multipliers_dict(self):
        setup_dict = {
                     'cha': (6.04, -0.14),
                     'bra': (-29.14, 0.71),
                     'ele': (6.11, -0.09),
                     }
        return setup_dict

    def setup_car_factor_gearbox_multipliers_dict(self):
        setup_dict = {
                     'gea': (-41, 1.09),
                     'ele': (9, -0.14),
                     }
        return setup_dict

    def setup_car_factor_suspension_multipliers_dict(self):
        setup_dict = {
                     'cha': (-15.27, 0.34),
                     'und': (-10.72, 0.23),
                     'sus': (31, -0.7),
                     'sid': (6.03, -0.12)
                     }
        return setup_dict

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
        print(mode, weather.mode)

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
        driver_factor = driver.tal * math.floor((base
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
        ws_wing_factor = ((car.fw['lvl'] + car.rw['lvl'])/2 
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
        return (track.data['eng_set'] + base_factor * driver.exp + factors[0])


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

    def fuel_calc_factors(self,track, driver, car, weather):
        self.fuel_factors_calc(driver, car, weather)
        for el in self.fuel_factors_dict.keys():
            mode = self.fuel_factors_dict[el][1]
            for fctr, mt in self.fuel_factors_dict[el][0].items():
                mf = mode[fctr]['lvl'] if el == 'car' else mode[fctr]
                to_add = track.fuel - track.fuel * ( mt ** (mf - track.data[fctr]))
                self.fuel_factors += -(to_add) if fctr == 'agg' else to_add

    def fuel_calc(self, track, weather, driver, car):
        self.fuel_calc_factors(track, driver, car, weather)
        track_fuel = (self.fuel_factors_calc + track.fuel) * 1.01
        return track_fuel, track_fuel * (track.wc + 0.01)
    

    """
    def tyre_factors_calc(self, driver, car, weather, track, tyre):
        self.fuel_factors_dict = {
            'driver': [
                {'agg': 0.999670155,'exp': 1.00022936,'wei': 0.999858329},
                driver.skill_dict ],
            'car': [{'sus': 1.009339294}, car.car_dict],
            'weather': [{'temp': 0.988463622}, weather.race],
            'track': [{'tyre_wear': 0.896416176238624}, track.data],
            'tyre': [{'durability': 1.048876356}, track.data],
        }
        self.tyre_factors = 0
    """

    
    def tyre_calc(self, track, weather, driver, car, tyre):
        tyre_wear_list = list()
        XS_MULT = 0.998163750229071
        S_MULT = 0.997064844817654
        M_MULT = 0.996380346554349
        H_MULT = 0.995862526048112
        R_MULT = 0.996087854384523
        MULTS = [XS_MULT, S_MULT, M_MULT, H_MULT, '', R_MULT]
        BASE = 129.776458172062
        WET_MULT = 0.73
        track_base = BASE * track.data['ctrack']
        wet_track_base = track_base * WET_MULT
        track_factor = 0.896416176238624 ** track.data['tyre_wear']
        temp_factor = 0.988463622 ** weather.race['temp']
        tyre_supp_factor = 1.048876356 ** tyre.durability
        sus_factor = 1.009339294 ** car.sus['lvl']
        agg_factor = 0.999670155 ** driver.agg
        exp_factor = 1.00022936 ** driver.exp
        wei_factor = 0.999858329 ** driver.wei
        risk = self.risk
        tyre_comp = 0
        for i in range(0,4):
            tyre_comp_factor = 1.390293715 ** tyre_comp
            risk_factor = MULTS[tyre_comp] ** risk
            mult = (track_factor * temp_factor * tyre_supp_factor * sus_factor
            * tyre_comp_factor * agg_factor * exp_factor * wei_factor * risk_factor)
            tyre_wear_list.append(track_base * mult)
            tyre_comp += 1
        tyre_comp = 5
        tyre_comp_factor = 1.390293715 ** tyre_comp
        risk_factor = MULTS[tyre_comp] ** risk
        mult = (track_factor * temp_factor * tyre_supp_factor * sus_factor
        * tyre_comp_factor * agg_factor * exp_factor * wei_factor * risk_factor)
        tyre_wear_list.append(wet_track_base * mult)
        return tyre_wear_list

    def part_wear_driv_factor(self, driver):
        con_factor = 0.998789138 ** driver.con
        tal_factor = 0.998751839 ** driver.tal
        exp_factor = 0.998707677 ** driver.exp
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