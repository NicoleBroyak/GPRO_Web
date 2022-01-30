from os import scandir
from django.db.models.fields import NullBooleanField
from django.http import request
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
import datetime
from gpro.forms import GPROForm
import time
from gpro.models import Race, Track, Season
from django import apps

class Scrapper():

    def __init__(self) -> None:
        self.scrap_count_consts()
        self.car_dict = dict()
        self.driver_stats = []
        self.calendar = dict()
        self.scrapper = self.scrapper_init()

    def scrapper_init(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=800,800')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        scrapper = webdriver.Chrome(options=chrome_options)
        return scrapper

    def reset_scrapper(self):
        self.scrapper.delete_all_cookies()
        self.scrapper.quit()
        self.scrapper = None
        self.scrapper = self.scrapper_init()
        

    def gpro_login(self, user, password):
        self.scrapper.get("https://gpro.net/pl/Login.asp")
        self.scrapper.find_element_by_name("textLogin").send_keys(user)
        self.scrapper.find_element_by_name("textPassword").send_keys(password)
        self.scrapper.find_element_by_name("LogonFake").click()
        page = self.soup_from_html('th')
        self.scrap_driver_name(page)

    def scrap_count_consts(self):
        self.CONST_DRIVER = set(range(15, 42, 3)).union({43, 47, 50})
        self.CONST_CAR_PARTS_NAMES = set(range(20, 86, 6))
        self.CONST_CAR_PARTS_LVL = set(range(21, 87, 6))
        self.CONST_CAR_PARTS_WEAR = set(range(23, 89, 6))

    def calendar_months_converter(self, date):
        calendar_dict = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12,
        }
        try:
            day = int(date[date.find(' ') + 1:date.find(',') - 2])
            month = calendar_dict[date[0:3]]
            year = int(date[-4:])
            date = datetime.date(year, month, day)
        except ValueError:
            date = datetime.date.today() - datetime.timedelta(days=1)
        return date

    def scrap_season_no(self, page_iter=3):
        self.scrapper.get("https://gpro.net/pl/gpro.asp")
        page = self.soup_from_html('h1')
        page = page[page_iter].text.strip()
        self.season = page[page.find('Sezon ') + 6:page.find(',')]
        return self.season

    def scrap_calendar_add_to_dict(self, td, count, gp_no):
        td = td.text.strip()
        if (count + 3) % 5 == 0:
            self.calendar[f'S{self.season}R{gp_no}'] = [td[:td.find(" GP")]]
        if (count + 2) % 5 == 0:
            date = self.calendar_months_converter(td)
            self.calendar[f'S{self.season}R{gp_no}'].append(date)
            race = Race(
                track=(Track.objects.get(name=self.calendar[f'S{self.season}R{gp_no}'][0])),
                season = (Season.objects.get(name=self.season)),
                identifier = gp_no,
                date = date)
            race.save()
            gp_no += 1
        return gp_no

    def scrap_calendar(self):
        self.scrap_season_no()
        self.scrapper.get("https://gpro.net/en/Calendar.asp")
        page = self.soup_from_html('td')
        gp_no, count = 1, 0
        for td in page:
            gp_no = self.scrap_calendar_add_to_dict(td, count, gp_no)
            if gp_no == 18: break
            count += 1

    def soup_from_html(self, elem=None):
        with open('page.html', 'w') as file:
            file.write(self.scrapper.page_source)
        p = open('page.html', 'r')
        page = p.read()
        soup = BeautifulSoup(page, "html.parser")
        if elem:
            tds = soup.find_all(elem)
            return tds
        return soup
    
    def load_page_to_scrap(self, text):
        self.scrapper.find_element_by_link_text(text).click()
        time.sleep(0.5)

    def scrap_driver_name(self, page):
        self.driver_name = page[0].text.strip()[10:]

    def scrap_driver(self):
        self.load_page_to_scrap(self.driver_name)
        tds = self.soup_from_html('td')
        count = 0
        for tr in tds:
            if count in self.CONST_DRIVER:
                self.driver_stats.append(int(tr.text.strip()))
            count += 1
        self.scrapper.back()
        return self.driver_stats

    def scrap_car(self):
        self.load_page_to_scrap('Modernizacja bolidu')
        tds = self.soup_from_html('td')
        count = 0
        for tr in tds:
            count += 1
            self.scrap_car_dict_create(count,tr,self.car_dict)
        self.scrapper.back()
        return self.car_dict

    def scrap_car_dict_create(self, count, tr, car_stats):
            if count in self.CONST_CAR_PARTS_NAMES:
                self.dictkey = str(tr.text.strip()).replace(':','')
            if count in self.CONST_CAR_PARTS_LVL:
                self.car_lvl = int(tr.text.strip())
            if count in self.CONST_CAR_PARTS_WEAR:
                self.car_wear = int(str(tr.text.strip()).replace("%",''))
                car_stats[self.dictkey] = {'lvl': self.car_lvl, 'wear': self.car_wear}

    def scrap_track_name_for_weather(self, i):
        track = str(i.text.strip())
        print(track)
        print("DONE")
        gp = track.find(" GP")
        whitespace = track.rfind('\t')
        track = track[whitespace + 1:gp]
        self.weather_dict['track'] = track
        print(track)
        print("DONE")

    def scrap_weather_for_q(self, tr, q):
        tr = str(tr)
        dependencies = (tr.find('alt="'), tr.find('Temp: '), tr.find('°'),
        tr.find('Wilgotność: '), tr.find('%'))
        weather = tr[dependencies[0] + 5]
        weather = 'wet' if weather == 'D' else 'dry'
        temp = int(str(tr)[dependencies[1] + 6:dependencies[2]])
        hum = int(str(tr)[dependencies[3] + 12:dependencies[4]])
        self.weather_dict[q] = {'weather': weather,'temp': temp,'hum': hum}

    def scrap_weather(self):
        self.weather_dict = dict()
        self.scrapper.find_element_by_link_text('Trening').click()
        tds = self.soup_from_html('td')
        h2 = self.soup_from_html('h2')
        self.scrap_track_name_for_weather(h2[1])
        self.scrap_weather_for_q(tds[5], 'q1')
        self.scrap_weather_for_q(tds[6], 'q2')
        self.scrapper.back()
        return self.weather_dict 

    def scrap_tyre(self):
        self.scrapper.find_element_by_link_text('Dostawcy opon').click()
        soup = self.soup_from_html()
        tds = soup.find(class_="column left chosen").text.strip()
        tyre_durability = int(tds[122])
        return tyre_durability

scrap = Scrapper()
#season = apps.apps.get_model('gpro', 'Season')
#scrap.scrap_calendar(scrapper)