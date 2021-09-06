import math

class Driver:
    def __init__(self):
        self.oa = 171  #to scrap
        self.con = 209
        self.tal = 202
        self.agg = 14
        self.exp = 174
        self.ti = 138
        self.sta = 214
        self.cha = 48
        self.mot = 245
        self.rep = 0
        self.wei = 46
        self.age = 30

class Car:
    def __init__(self):
        self.cha = {"lvl": 6, "wear": 37}
        self.eng = {"lvl": 2, "wear": 64}
        self.fw = {"lvl": 5, "wear": 67}
        self.rw = {"lvl": 5, "wear": 12}
        self.und = {"lvl": 5, "wear": 34}
        self.sid = {"lvl": 6, "wear": 67}
        self.coo = {"lvl": 6, "wear": 65}
        self.gea = {"lvl": 3, "wear": 12}
        self.bra = {"lvl": 6, "wear": 58}
        self.sus = {"lvl": 5, "wear": 65}
        self.ele = {"lvl": 7, "wear": 23}

class Weather:
    def __init__(self):
        self.q1 = {"weather": "dry", "temp": 17, "hum": 11}
        self.race = {"weather": "wet", "temp": 12, "hum": 11}

class Track:
    def __init__(self):
        self.pow = 5
        self.han = 10
        self.acc = 7
        self.downforce = 2
        self.overtaking = 2
        self.sus = 0
        self.corners = 10
        self.lenght = 3.04
        self.laps = 80
        self.tyre_wear = 3
        self.fuel_wear = 2
        self.ctrack = 96.6226944537927/100
        self.ws = 236.704044068807
        self.wings = 1002.72335509463
        self.eng = 460.626256188571
        self.bra = 699.986666666667
        self.gea = 764
        self.sus = 244.47
        self.fuel = 173
        self.con = 201
        self.agg = 0
        self.exp = 23
        self.ti = 95
        self.englvl = 6
        self.ele = 4
        self.hum = 8
        self.wc = 81.5446778637633/100

class Tyre:
    def __init__(self):
        self.durability = 8

class Calcs:
    def __init__(self):
        pass

    def wings_calc(self, track, weather, driver, car):
        base = track.wings * 2
        dry_factor = weather.race['temp'] * 12
        wet_factor = (weather.race['temp'] + 263) * 2
        car_lvl_factor = 30.03 * (car.fw['lvl']
        + car.rw['lvl']) + (-19.74 * car.cha['lvl']
        + -15.07 * car.und['lvl'])
        car_wear_factor = -0.59 * (car.fw['wear']
        + car.rw['wear']) + (0.47 * car.cha['wear']
        + 0.32 * car.und['wear'])
        if weather.race['weather'] == 'dry':
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

    def ws_calc(self, track, weather, driver, car):
        ws_wing_factor = ((car.fw['lvl'] + car.rw['lvl'])/2 
        * 3.69107049712848)
        ws_tal_factor = driver.tal * -0.246534498671854
        ws_weather_factor = weather.race['temp'] * 0.376337780506523
        ws_setup_factor = (Calcs.wings_calc(Calcs, track, weather, driver, car)
        * -0.189968386659174)
        ws_dry = (track.ws + ws_tal_factor
                 + ws_wing_factor + ws_weather_factor + ws_setup_factor)
        if weather.race['weather'] == 'dry':
            return ws_dry
        return ws_dry + 58.8818967363256

    def eng_calc(self, track, weather, driver, car):
        base = track.eng
        aggr_factor = driver.agg * 0.29521804804429
        car_lvl_factor = car.eng['lvl'] * 16.04 + (car.coo['lvl'] * 4.9
        + car.ele['lvl'] * 3.34)
        car_wear_factor = car.eng['wear'] * -0.51 + (car.coo['wear']
        * -0.09 + car.ele['wear'] * -0.04)
        car_factor = car_lvl_factor + car_wear_factor
        if weather.race['weather'] == 'dry':
            weather_factor = weather.race['temp'] * -3
            base_dry = base + weather_factor
            base_factor = base_dry * 0.001655723 + 0.0469416263186552
        else:
            weather_factor = weather.race['temp'] * 0.7 - 190
            base_wet = base + weather_factor
            base_factor = base_wet * 0.001655723 + 0.0469416263186552
        eng = (base + aggr_factor + base_factor 
              * driver.exp + car_factor + weather_factor)
        return eng

    def bra_calc(self, track, weather, driver, car):
        base = track.bra
        tal_factor = driver.tal * -0.498
        car_lvl_factor = car.cha['lvl'] * 6.04 + (car.bra['lvl']
        * -29.14 + car.ele['lvl'] * 6.11)
        car_wear_factor = car.cha['wear'] * -0.14 + (car.bra['wear']
        * 0.71 + car.ele['wear'] * -0.09)
        car_factor = car_lvl_factor + car_wear_factor
        if weather.race['weather'] == 'dry':
            weather_factor = weather.race['temp'] * 6
        else:
            weather_factor = (
            weather.race['temp'] * 3.9883754414027 + 105.532592432347)
        bra = base + tal_factor + car_factor + weather_factor
        return bra

    def gea_calc(self, track, weather, driver, car):
        base = track.gea
        con_factor = driver.con / 2
        car_lvl_factor = car.gea['lvl'] * -41 + car.ele['lvl'] * 9
        car_wear_factor = car.gea['wear'] * 1.09 + car.ele['wear'] * -0.14
        car_factor = car_lvl_factor + car_wear_factor
        if weather.race['weather'] == 'dry':
            weather_factor = weather.race['temp'] * -4
        else:
            weather_factor = (
            weather.race['temp'] * -8.01996418151657 - 4.74271170354302)
        gea = base + con_factor + car_factor + weather_factor
        return gea

    def sus_calc(self, track, weather, driver, car):
        base = track.sus
        dri_factor = driver.wei * 2 + driver.exp * 0.75
        car_lvl_factor = ((car.cha['lvl'] * -15.27) + (car.und['lvl'] * -10.72)
        + (car.sus['lvl'] * 31) + (car.sid['lvl'] * 6.03))
        car_wear_factor = ((car.cha['wear'] * 0.34) + (car.und['wear'] * 0.23)
        + (car.sus['wear'] * -0.7) + (car.sid['wear'] * -0.12))
        car_factor = car_lvl_factor + car_wear_factor
        if weather.race['weather'] == 'dry':
            weather_factor = weather.race['temp'] * -6
        else:
            dri_factor = dri_factor + driver.ti * 0.11
            weather_factor = -257 + -1 * (weather.race['temp'])
            print(weather_factor)
        sus = base + dri_factor + car_factor + weather_factor
        return sus

    def fuel_calc(self, track, weather, driver, car):
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
        if weather.race['weather'] == 'dry':
            return track_fuel
        return track_fuel * (track.wc + 0.01)
    
    def tyre_calc(self, track, weather, driver, car, tyre):
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
        tyre_comp = int(input('tyre compound'))
        tyre_comp_factor = 1.390293715 ** tyre_comp
        sus_factor = 1.009339294 ** car.sus['lvl']
        agg_factor = 0.999670155 ** driver.agg
        exp_factor = 1.00022936 ** driver.exp
        wei_factor = 0.999858329 ** driver.wei
        risk_factor = MULTS[tyre_comp] ** int(input('risk'))
        mult = (track_factor * temp_factor * tyre_supp_factor * sus_factor
         * tyre_comp_factor * agg_factor * exp_factor * wei_factor * risk_factor)
        if weather.race['weather'] == 'dry':
            return track_base * mult
        return wet_track_base * mult


track = Track()
weather = Weather()
driver = Driver()
car = Car()
tyre = Tyre()
wing_split = Calcs.ws_calc(Calcs, track, weather, driver, car)
wing_setup = Calcs.wings_calc(Calcs, track, weather, driver, car)
eng = Calcs.eng_calc(Calcs, track, weather, driver, car)
bra = Calcs.bra_calc(Calcs, track, weather, driver, car)
gea = Calcs.gea_calc(Calcs, track, weather, driver, car)
sus = Calcs.sus_calc(Calcs, track, weather, driver, car)
fuel = Calcs.fuel_calc(Calcs, track, weather, driver, car)
tyre = Calcs.tyre_calc(Calcs, track, weather, driver, car, tyre)
fw = wing_setup + wing_split
rw = wing_setup - wing_split
print(fw)
print(rw)
print(eng)
print(bra)
print(gea)
print(sus)
print(tyre)
print(fuel)