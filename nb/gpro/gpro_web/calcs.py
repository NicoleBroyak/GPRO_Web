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
        name = weather.weather_data['track']
        data = trackdata[name]
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
        self.englvl = data['eng_lvl']
        self.ele = data['ele_lvl']
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
        base = track.wings * 2
        car_lvl_factor, car_wear_factor = self.setup_car_factor(car, 'wings')
        weather_factor = self.setup_weather_factor(weather, 'wings', mode)
        driver_factor = self.wings_calc_driver_factor(driver, base, weather_factor)
        wings = (track.wings * 2 + weather_factor + (driver_factor
        + car_lvl_factor) + car_wear_factor)/2
        return wings

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
        ws = (track.ws + ws_calc_factors[1]
            + ws_calc_factors[0] + ws_calc_factors[2] + ws_calc_factors[3])
        if weather.mode['weather'] == 'dry':
            return ws
        return ws + 58.8818967363256

    def eng_calc(self, track, weather, driver, car, mode=''):
        driver_factor = self.setup_driver_factor(driver, 'eng')
        car_lvl_factor, car_wear_factor = self.setup_car_factor(car, 'eng')
        car_factor = car_lvl_factor + car_wear_factor
        weather_factor = self.setup_weather_factor(weather, 'eng', mode)
        base_factor = (track.eng + weather_factor) * 0.001655723 + 0.0469416263186552
        return (track.eng + driver_factor + base_factor 
              * driver.exp + car_factor + weather_factor)

    def bra_calc(self, track, weather, driver, car, mode=''):
        driver_factor = self.setup_driver_factor(driver, 'bra')
        car_lvl_factor, car_wear_factor = self.setup_car_factor(car, 'bra')
        car_factor = car_lvl_factor + car_wear_factor
        weather_factor = self.setup_weather_factor(weather, 'bra', mode)
        return track.bra + driver_factor + car_factor + weather_factor

    def gea_calc(self, track, weather, driver, car, mode=''):
        base = track.gea
        driver_factor = self.setup_driver_factor(driver, 'gea')
        car_lvl_factor, car_wear_factor = self.setup_car_factor(car, 'gea')
        car_factor = car_lvl_factor + car_wear_factor
        weather_factor = self.setup_weather_factor(weather, 'gea', mode)
        return base + driver_factor + car_factor + weather_factor

    def sus_calc(self, track, weather, driver, car, mode=''):
        dri_factor = self.setup_driver_factor(driver, 'sus')
        car_lvl_factor, car_wear_factor = self.setup_car_factor(car, 'sus')
        car_factor = car_lvl_factor + car_wear_factor
        weather_factor = self.setup_weather_factor(weather, 'sus', mode)
        return track.sus + dri_factor + car_factor + weather_factor

    def fuel_calc(self, track, weather, driver, car):
        fuel_calc_list = list()
        track_fuel = track.fuel
        con_factor = track_fuel - track_fuel * (1.00008
        ** (driver.con - track.con))
        agg_factor = -(track_fuel - track_fuel * (1.00018
        ** (driver.agg - track.agg)))
        exp_factor = track_fuel - track_fuel * (1.00014
        ** (driver.exp - track.exp))
        ti_factor = track_fuel - track_fuel * (1.00036
        ** (driver.ti - track.ti))
        eng_factor = track_fuel - track_fuel * (1.014
        ** (car.eng['lvl'] - track.englvl))
        ele_factor = track_fuel - track_fuel * (1.009
        ** (car.ele['lvl'] - track.ele))
        hum_factor = track_fuel - track_fuel * (1.00025
        ** (weather.race['hum'] - track.hum))
        track_fuel = (con_factor + agg_factor + exp_factor + ti_factor
        + eng_factor + ele_factor + hum_factor + track_fuel) * 1.01
        fuel_calc_list.append(track_fuel)
        fuel_calc_list.append(track_fuel * (track.wc + 0.01))
        return fuel_calc_list
    
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
        track_base = BASE * track.ctrack
        wet_track_base = track_base * WET_MULT
        track_factor = 0.896416176238624 ** track.tyre_wear
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

    def cha_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.cha['lvl']]
        risk_factor = lvl_factor ** self.risk
        return driv_factor * risk_factor * track.cha_wear 

    def eng_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.eng['lvl']]
        risk_factor = lvl_factor ** self.risk
        return driv_factor * risk_factor * track.eng_wear 

    def fw_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.fw['lvl']]
        risk_factor = lvl_factor ** self.risk
        return driv_factor * risk_factor * track.fw_wear 

    def rw_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.rw['lvl']]
        risk_factor = lvl_factor ** self.risk
        rw_wear = driv_factor * risk_factor * track.rw_wear 
        return rw_wear

    def und_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.und['lvl']]
        risk_factor = lvl_factor ** self.risk
        und_wear = driv_factor * risk_factor * track.und_wear 
        return und_wear

    def sid_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.sid['lvl']]
        risk_factor = lvl_factor ** self.risk
        return driv_factor * risk_factor * track.sid_wear 

    def coo_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.coo['lvl']]
        risk_factor = lvl_factor ** self.risk
        return driv_factor * risk_factor * track.coo_wear 

    def gea_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.gea['lvl']]
        risk_factor = lvl_factor ** self.risk
        return driv_factor * risk_factor * track.gea_wear 

    def bra_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.bra['lvl']]
        risk_factor = lvl_factor ** self.risk
        return driv_factor * risk_factor * track.bra_wear 

    def sus_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.sus['lvl']]
        risk_factor = lvl_factor ** self.risk
        return driv_factor * risk_factor * track.sus_wear 

    def ele_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.ele['lvl']]
        risk_factor = lvl_factor ** self.risk 
        return driv_factor * risk_factor * track.ele_wear 

    def part_wear(self, track, driver, car):
        driv_factor = self.part_wear_driv_factor(driver)
        part_wear = dict()
        part_wear['cha'] = [
            round(self.cha_wear_calc(track, car, driv_factor)),
            round(self.cha_wear_calc(track, car, driv_factor) + car.cha['wear'])
            ] 
        part_wear['eng'] = [
            round(self.eng_wear_calc(track, car, driv_factor)),
            round(self.eng_wear_calc(track, car, driv_factor) + car.eng['wear'])
            ] 
        part_wear['fw'] = [
            round(self.fw_wear_calc(track, car, driv_factor)),
            round(self.fw_wear_calc(track, car, driv_factor) + car.fw['wear'])
            ] 
        part_wear['rw'] = [
            round(self.rw_wear_calc(track, car, driv_factor)),
            round(self.rw_wear_calc(track, car, driv_factor) + car.rw['wear'])
            ]                                     
        part_wear['und'] = [
            round(self.und_wear_calc(track, car, driv_factor)),
            round(self.und_wear_calc(track, car, driv_factor) + car.und['wear'])
            ] 
        part_wear['sid'] = [
            round(self.sid_wear_calc(track, car, driv_factor)),
            round(self.sid_wear_calc(track, car, driv_factor) + car.sid['wear'])
            ] 
        part_wear['coo'] = [
            round(self.coo_wear_calc(track, car, driv_factor)),
            round(self.coo_wear_calc(track, car, driv_factor) + car.coo['wear'])
            ] 
        part_wear['gea'] = [
            round(self.gea_wear_calc(track, car, driv_factor)),
            round(self.gea_wear_calc(track, car, driv_factor) + car.gea['wear'])
            ] 
        part_wear['bra'] = [
            round(self.bra_wear_calc(track, car, driv_factor)),
            round(self.bra_wear_calc(track, car, driv_factor) + car.bra['wear'])
            ] 
        part_wear['sus'] = [
            round(self.sus_wear_calc(track, car, driv_factor)),
            round(self.sus_wear_calc(track, car, driv_factor) + car.sus['wear'])
            ] 
        part_wear['ele'] = [
            round(self.ele_wear_calc(track, car, driv_factor)),
            round(self.ele_wear_calc(track, car, driv_factor) + car.ele['wear'])
            ] 
        return part_wear