import math
from seleniumscrap import *
from track import trackdata
from partwear import partwear_lvl_factor
class Driver:
    def __init__(self):
        driver_stats = scrap_driver(scrapper)
        self.oa = driver_stats[0]
        self.con = driver_stats[1]
        self.tal = driver_stats[2]
        self.agg = driver_stats[3]
        self.exp = driver_stats[4]
        self.ti = driver_stats[5]
        self.sta = driver_stats[6]
        self.cha = driver_stats[7]
        self.mot = driver_stats[8]
        self.rep = driver_stats[9]
        self.wei = driver_stats[10]
        self.age = driver_stats[11]

class Car:
    def __init__(self):
        car_stats = scrap_car(scrapper)
        self.cha = car_stats['Nadwozie']
        self.eng = car_stats['Silnik']
        self.fw = car_stats['Przednie skrzydło']
        self.rw = car_stats['Tylne skrzydło']
        self.und = car_stats['Podwozie']
        self.sid = car_stats['Wloty powietrza']
        self.coo = car_stats['Chłodzenie']
        self.gea = car_stats['Skrzynia biegów']
        self.bra = car_stats['Hamulce']
        self.sus = car_stats['Zawieszenie']
        self.ele = car_stats['Elektronika']

class Weather:
    def __init__(self):
        self.weather_data = scrap_weather(scrapper)
        self.q1 = self.weather_data['q1']
        self.q2 = self.weather_data['q2']
        self.race = {'weather': 'dry', 'temp': 31, 'hum': 55}

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
        self.durability = 8

class Calcs:
    def __init__(self):
        self.risk = int(input('Risk:'))

    def wings_calc(self, track, weather, driver, car, mode=''):
        if mode == "q2":
            weather.mode = weather.q2
        elif mode == 'race':
            weather.mode = weather.race
        else:
            weather.mode = weather.q1
        base = track.wings * 2
        dry_factor = weather.mode['temp'] * 12
        wet_factor = (weather.mode['temp'] + 263) * 2
        car_lvl_factor = 30.03 * (car.fw['lvl']
        + car.rw['lvl']) + (-19.74 * car.cha['lvl']
        + -15.07 * car.und['lvl'])
        car_wear_factor = -0.59 * (car.fw['wear']
        + car.rw['wear']) + (0.47 * car.cha['wear']
        + 0.32 * car.und['wear'])
        if weather.mode['weather'] == 'dry':
            driver_factor = driver.tal * math.floor((base
            + dry_factor)) * -0.001349079032746
            wings = (base + dry_factor + (driver_factor
            + car_lvl_factor) + car_wear_factor)/2
            return wings
        driver_factor = driver.tal * math.floor((base
        + wet_factor)) * -0.001349079032746
        wings = (base + wet_factor + (driver_factor
        + car_lvl_factor) + car_wear_factor)/2
        return wings

    def ws_calc(self, track, weather, driver, car, mode=''):
        if mode == "q2":
            weather.mode = weather.q2
        elif mode == 'race':
            weather.mode = weather.race
        else:
            weather.mode = weather.q1
        ws_wing_factor = ((car.fw['lvl'] + car.rw['lvl'])/2 
        * 3.69107049712848)
        ws_tal_factor = driver.tal * -0.246534498671854
        ws_weather_factor = weather.mode['temp'] * 0.376337780506523
        ws_setup_factor = (self.wings_calc(track, weather, driver, car
        ,mode) * -0.189968386659174)
        ws_dry = (track.ws + ws_tal_factor
                 + ws_wing_factor + ws_weather_factor + ws_setup_factor)
        if weather.mode['weather'] == 'dry':
            return ws_dry
        return ws_dry + 58.8818967363256

    def eng_calc(self, track, weather, driver, car, mode=''):
        if mode == "q2":
            weather.mode = weather.q2
        elif mode == 'race':
            weather.mode = weather.race
        else:
            weather.mode = weather.q1
        base = track.eng
        aggr_factor = driver.agg * 0.29521804804429
        car_lvl_factor = car.eng['lvl'] * 16.04 + (car.coo['lvl'] * 4.9
        + car.ele['lvl'] * 3.34)
        car_wear_factor = car.eng['wear'] * -0.51 + (car.coo['wear']
        * -0.09 + car.ele['wear'] * -0.04)
        car_factor = car_lvl_factor + car_wear_factor
        if weather.mode['weather'] == 'dry':
            weather_factor = weather.mode['temp'] * -3
            base_dry = base + weather_factor
            base_factor = base_dry * 0.001655723 + 0.0469416263186552
        else:
            weather_factor = weather.mode['temp'] * 0.7 - 190
            base_wet = base + weather_factor
            base_factor = base_wet * 0.001655723 + 0.0469416263186552
        eng = (base + aggr_factor + base_factor 
              * driver.exp + car_factor + weather_factor)
        return eng

    def bra_calc(self, track, weather, driver, car, mode=''):
        if mode == "q2":
            weather.mode = weather.q2
        elif mode == 'race':
            weather.mode = weather.race
        else:
            weather.mode = weather.q1
        base = track.bra
        tal_factor = driver.tal * -0.498
        car_lvl_factor = car.cha['lvl'] * 6.04 + (car.bra['lvl']
        * -29.14 + car.ele['lvl'] * 6.11)
        car_wear_factor = car.cha['wear'] * -0.14 + (car.bra['wear']
        * 0.71 + car.ele['wear'] * -0.09)
        car_factor = car_lvl_factor + car_wear_factor
        if weather.mode['weather'] == 'dry':
            weather_factor = weather.mode['temp'] * 6
        else:
            weather_factor = (
            weather.mode['temp'] * 3.9883754414027 + 105.532592432347)
        bra = base + tal_factor + car_factor + weather_factor
        return bra

    def gea_calc(self, track, weather, driver, car, mode=''):
        if mode == "q2":
            weather.mode = weather.q2
        elif mode == 'race':
            weather.mode = weather.race
        else:
            weather.mode = weather.q1
        base = track.gea
        con_factor = driver.con / 2
        car_lvl_factor = car.gea['lvl'] * -41 + car.ele['lvl'] * 9
        car_wear_factor = car.gea['wear'] * 1.09 + car.ele['wear'] * -0.14
        car_factor = car_lvl_factor + car_wear_factor
        if weather.mode['weather'] == 'dry':
            weather_factor = weather.mode['temp'] * -4
        else:
            weather_factor = (
            weather.mode['temp'] * -8.01996418151657 - 4.74271170354302)
        gea = base + con_factor + car_factor + weather_factor
        return gea

    def sus_calc(self, track, weather, driver, car, mode=''):
        if mode == "q2":
            weather.mode = weather.q2
        elif mode == 'race':
            weather.mode = weather.race
        else:
            weather.mode = weather.q1
        base = track.sus
        dri_factor = driver.wei * 2 + driver.exp * 0.75
        car_lvl_factor = ((car.cha['lvl'] * -15.27) + (car.und['lvl'] * -10.72)
        + (car.sus['lvl'] * 31) + (car.sid['lvl'] * 6.03))
        car_wear_factor = ((car.cha['wear'] * 0.34) + (car.und['wear'] * 0.23)
        + (car.sus['wear'] * -0.7) + (car.sid['wear'] * -0.12))
        car_factor = car_lvl_factor + car_wear_factor
        if weather.mode['weather'] == 'dry':
            weather_factor = weather.mode['temp'] * -6
        else:
            dri_factor = dri_factor + driver.ti * 0.11
            weather_factor = -257 + -1 * (weather.mode['temp'])
            print(weather_factor)
        sus = base + dri_factor + car_factor + weather_factor
        return sus

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
        cha_wear = driv_factor * risk_factor * track.cha_wear 
        return cha_wear

    def eng_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.eng['lvl']]
        risk_factor = lvl_factor ** self.risk
        eng_wear = driv_factor * risk_factor * track.eng_wear 
        return eng_wear

    def fw_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.fw['lvl']]
        risk_factor = lvl_factor ** self.risk
        fw_wear = driv_factor * risk_factor * track.fw_wear 
        return fw_wear

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
        sid_wear = driv_factor * risk_factor * track.sid_wear 
        return sid_wear

    def coo_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.coo['lvl']]
        risk_factor = lvl_factor ** self.risk
        coo_wear = driv_factor * risk_factor * track.coo_wear 
        return coo_wear

    def gea_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.gea['lvl']]
        risk_factor = lvl_factor ** self.risk
        gea_wear = driv_factor * risk_factor * track.gea_wear 
        return gea_wear

    def bra_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.bra['lvl']]
        risk_factor = lvl_factor ** self.risk
        bra_wear = driv_factor * risk_factor * track.bra_wear 
        return bra_wear

    def sus_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.sus['lvl']]
        risk_factor = lvl_factor ** self.risk
        sus_wear = driv_factor * risk_factor * track.sus_wear 
        return sus_wear

    def ele_wear_calc(self, track, car, driv_factor):
        lvl_factor = partwear_lvl_factor[car.ele['lvl']]
        risk_factor = lvl_factor ** self.risk
        ele_wear = driv_factor * risk_factor * track.ele_wear 
        return ele_wear

    def part_wear(self, track, driver, car):
        driv_factor = self.part_wear_driv_factor(driver)
        part_wear = dict()
        part_wear['cha'] = self.cha_wear_calc(track, car, driv_factor)
        part_wear['eng'] = self.eng_wear_calc(track, car, driv_factor)
        part_wear['fw'] = self.fw_wear_calc(track, car, driv_factor)
        part_wear['rw'] = self.rw_wear_calc(track, car, driv_factor)
        part_wear['und'] = self.und_wear_calc(track, car, driv_factor)
        part_wear['sid'] = self.sid_wear_calc(track, car, driv_factor)
        part_wear['coo'] = self.coo_wear_calc(track, car, driv_factor)
        part_wear['gea'] = self.gea_wear_calc(track, car, driv_factor)
        part_wear['bra'] = self.bra_wear_calc(track, car, driv_factor)
        part_wear['sus'] = self.sus_wear_calc(track, car, driv_factor)
        part_wear['ele'] = self.ele_wear_calc(track, car, driv_factor)
        return part_wear



gpro_login(scrapper)
weather = Weather()
print(weather.weather_data)
track = Track(weather)
driver = Driver()
car = Car()
tyre = Tyre()
calcs = Calcs()
scrapper.quit()
wing_split = calcs.ws_calc(track, weather, driver, car)
wing_setup = calcs.wings_calc(track, weather, driver, car)
eng = calcs.eng_calc(track, weather, driver, car)
bra = calcs.bra_calc(track, weather, driver, car)
gea = calcs.gea_calc(track, weather, driver, car)
sus = calcs.sus_calc(track, weather, driver, car)
wing_splitq2 = calcs.ws_calc(track, weather, driver, car, mode='q2')
wing_setupq2 = calcs.wings_calc(track, weather, driver, car, mode='q2')
engq2 = calcs.eng_calc(track, weather, driver, car, mode='q2')
braq2 = calcs.bra_calc(track, weather, driver, car, mode='q2')
geaq2 = calcs.gea_calc(track, weather, driver, car, mode='q2')
susq2 = calcs.sus_calc(track, weather, driver, car, mode='q2')
wing_splitr = calcs.ws_calc(track, weather, driver, car, mode='race')
wing_setupr = calcs.wings_calc(track, weather, driver, car, mode='race')
engr = calcs.eng_calc(track, weather, driver, car, mode='race')
brar = calcs.bra_calc(track, weather, driver, car, mode='race')
gear = calcs.gea_calc(track, weather, driver, car, mode='race')
susr = calcs.sus_calc(track, weather, driver, car, mode='race')
fuel = calcs.fuel_calc(track, weather, driver, car)
tyre = calcs.tyre_calc(track, weather, driver, car, tyre)
fw = wing_setup + wing_split
rw = wing_setup - wing_split
fwq2 = wing_setupq2 + wing_splitq2
rwq2 = wing_setupq2 - wing_splitq2
fwr = wing_setupr + wing_splitr
rwr = wing_setupr - wing_splitr
print("q1", "q2", "race")
print(round(fw), round(fwq2), round(fwr))
print(round(rw), round(rwq2), round(rwr))
print(round(eng), round(engq2), round(engr))
print(round(bra), round(braq2), round(brar))
print(round(gea), round(geaq2), round(gear))
print(round(sus), round(susq2), round(susr))
print(f'tyre max distance: XS: {tyre[0]}'
      f'S: {tyre[1]}, M: {tyre[2]}, H: {tyre[3]}, R: {tyre[4]}')
print(fuel)
print(math.floor(tyre[0]/track.length))
print(math.floor(tyre[1]/track.length))
print(math.floor(tyre[2]/track.length))
print(math.floor(tyre[3]/track.length))
print(math.floor(tyre[4]/track.length))
partwear = calcs.part_wear(track, driver, car)
print("Part\tLvl\tBefore race\tWear\tAfter Race")
print(f"Chassis\t{car.cha['lvl']}\t{car.cha['wear']}\t"
      f"{round(partwear['cha'])}\t{car.cha['wear'] + round(partwear['cha'])}")
print(f"Engine\t{car.eng['lvl']}\t{car.eng['wear']}\t"
      f"{round(partwear['eng'])}\t{car.eng['wear'] + round(partwear['eng'])}")
print(f"FW\t{car.fw['lvl']}\t{car.fw['wear']}\t"
      f"{round(partwear['fw'])}\t{car.fw['wear'] + round(partwear['fw'])}")
print(f"RW\t{car.rw['lvl']}\t{car.rw['wear']}\t"
      f"{round(partwear['rw'])}\t{car.rw['wear'] + round(partwear['rw'])}")
print(f"Und\t{car.und['lvl']}\t{car.und['wear']}\t"
      f"{round(partwear['und'])}\t{car.und['wear'] + round(partwear['und'])}")
print(f"Sid\t{car.sid['lvl']}\t{car.sid['wear']}\t"
      f"{round(partwear['sid'])}\t{car.sid['wear'] + round(partwear['sid'])}")
print(f"Cooling\t{car.coo['lvl']}\t{car.coo['wear']}\t"
      f"{round(partwear['coo'])}\t{car.coo['wear'] + round(partwear['coo'])}")
print(f"Gearbox\t{car.gea['lvl']}\t{car.gea['wear']}\t"
      f"{round(partwear['gea'])}\t{car.gea['wear'] + round(partwear['gea'])}")
print(f"Brakes\t{car.bra['lvl']}\t{car.bra['wear']}\t"
      f"{round(partwear['bra'])}\t{car.bra['wear'] + round(partwear['bra'])}")
print(f"Susp\t{car.sus['lvl']}\t{car.sus['wear']}\t"
      f"{round(partwear['sus'])}\t{car.sus['wear'] + round(partwear['sus'])}")
print(f"Elec\t{car.ele['lvl']}\t{car.ele['wear']}\t"
      f"{round(partwear['ele'])}\t{car.ele['wear'] + round(partwear['ele'])}")