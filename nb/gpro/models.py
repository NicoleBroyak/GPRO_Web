from django.db import models
 
 
class Season(models.Model):
    name = models.IntegerField(unique=True)
 
    class Meta:
        verbose_name = "Sezon"
        verbose_name_plural = "Sezony"
 
    def __str__(self):
        return f'Sezon {self.name}'
 
 
class Track(models.Model):
    name = models.CharField(max_length=128, verbose_name="Nazwa toru", unique=True)
 
    class Meta:
        verbose_name = "Tor"
        verbose_name_plural = "Tory"
 
    def __str__(self):
        return f'Tor {self.name}'
 
 
class Race(models.Model):
    track = models.ForeignKey('gpro.Track',to_field='name', on_delete=models.PROTECT, verbose_name="Tor")
    season = models.ForeignKey('gpro.Season',to_field='name', on_delete=models.PROTECT, verbose_name="Sezon")
    identifier = models.IntegerField()
    date = models.DateField(verbose_name="Data wyścigu")
 
    class Meta:
        verbose_name = "Wyścig"
        verbose_name_plural = "Wyścigi"
 
    def __str__(self):
        return f'Wyścig S{self.season.name}R{self.identifier}'

class Calc_Data(models.Model):
    track = models.ForeignKey('gpro.Track',to_field='name', on_delete=models.PROTECT, verbose_name="Tor")
    season = models.ForeignKey('gpro.Season',to_field='name', on_delete=models.PROTECT, verbose_name="Sezon")
    dri_oa = models.IntegerField(verbose_name="Overall")
    dri_con = models.IntegerField(verbose_name="Concentration")
    dri_tal = models.IntegerField(verbose_name="Talent")
    dri_agg = models.IntegerField(verbose_name="Aggressiveness")
    dri_exp = models.IntegerField(verbose_name="Experience")
    dri_ti = models.IntegerField(verbose_name="Technical Insight")
    dri_sta = models.IntegerField(verbose_name="Stamina")
    dri_cha = models.IntegerField(verbose_name="Charisma")
    dri_mot = models.IntegerField(verbose_name="Motivation")
    dri_rep = models.IntegerField(verbose_name="Reputation")
    dri_wei = models.IntegerField(verbose_name="Weight")
    dri_age = models.IntegerField(verbose_name="Age")
    car_cha_lvl = models.IntegerField(verbose_name="Chassis lvl")
    car_cha_wear = models.IntegerField(verbose_name="Chassis Wear")
    car_eng_lvl = models.IntegerField(verbose_name="Engine lvl")
    car_eng_wear = models.IntegerField(verbose_name="Engine Wear")
    car_fw_lvl = models.IntegerField(verbose_name="Front wing lvl")
    car_fw_wear = models.IntegerField(verbose_name="Front Wing Wear")
    car_rw_lvl = models.IntegerField(verbose_name="Rear wing lvl")
    car_rw_wear = models.IntegerField(verbose_name="Rear wing Wear")
    car_und_lvl = models.IntegerField(verbose_name="Underbody lvl")
    car_und_wear = models.IntegerField(verbose_name="Underbody Wear")
    car_sid_lvl = models.IntegerField(verbose_name="Sidepods lvl")
    car_sid_wear = models.IntegerField(verbose_name="Sidepods Wear")
    car_coo_lvl = models.IntegerField(verbose_name="Colling lvl")
    car_coo_wear = models.IntegerField(verbose_name="Cooling Wear")
    car_gea_lvl = models.IntegerField(verbose_name="Gearbox lvl")
    car_gea_wear = models.IntegerField(verbose_name="Gearbox Wear")
    car_bra_lvl = models.IntegerField(verbose_name="Brakes lvl")
    car_bra_wear = models.IntegerField(verbose_name="Brakes Wear")
    car_sus_lvl = models.IntegerField(verbose_name="Suspension lvl")
    car_sus_wear = models.IntegerField(verbose_name="Suspension Wear")
    car_ele_lvl = models.IntegerField(verbose_name="Electronics lvl")
    car_ele_wear = models.IntegerField(verbose_name="Electronics Wear")
    xs_wear = models.FloatField(verbose_name="Extra soft wear")
    s_wear = models.FloatField(verbose_name="Soft wear")
    m_wear = models.FloatField(verbose_name="Medium wear")
    h_wear = models.FloatField(verbose_name="Hard wear")
    r_wear = models.FloatField(verbose_name="Rain wear")
    fuel_dry_wear = models.FloatField(verbose_name="Fuel dry wear")
    fuel_wet_wear = models.FloatField(verbose_name="Fuel wet wear")
    risk = models.IntegerField(verbose_name="Risk")
    temp = models.IntegerField(verbose_name="Temperature")
    hum = models.IntegerField(verbose_name="Humidity")


    
