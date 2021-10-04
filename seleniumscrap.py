from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver

def gpro_login(scrapper):
    user = input('User')
    password = input("Password")
    scrapper.get("https://gpro.net/pl/Login.asp")
    scrapper.find_element_by_name("textLogin").send_keys(user)
    scrapper.find_element_by_name("textPassword").send_keys(password)
    scrapper.find_element_by_name("LogonFake").click()

def scrap_driver(scrapper):
    scrapper.find_element_by_link_text('Damien Bailey').click()
    with open('page.html', 'w') as file:
        file.write(scrapper.page_source)
    p = open('page.html', 'r')
    page = p.read()
    soup = BeautifulSoup(page, "html.parser")
    tds = soup.find_all("td")
    count = 0
    driver_stats = []
    for tr in tds:
        if count % 3 == 0 and count > 12 and count < 40:
            driver_stats.append(int(tr.text.strip()))
        elif count == 43 or count == 47 or count == 50:
            driver_stats.append(int(tr.text.strip()))
        count += 1
    scrapper.back()
    return driver_stats

def scrap_car(scrapper):
    scrapper.find_element_by_link_text('Modernizacja bolidu').click()
    with open('page.html', 'w') as file:
        file.write(scrapper.page_source)
    p = open('page.html', 'r')
    page = p.read()
    soup = BeautifulSoup(page, "html.parser")
    tds = soup.find_all("td")
    count = 0
    car_stats = dict()
    for tr in tds:
        count += 1
        if (count + 4) % 6 == 0 and count > 7 and count < 69:
            dictkey = str(tr.text.strip()).replace(':','')
        if (count + 3) % 6 == 0 and count > 8 and count < 70:
            temp = int(tr.text.strip())
        if (count + 1) % 6 == 0 and count > 10 and count < 72:
            temp2 = str(tr.text.strip()).replace("%",'')
            car_stats[dictkey] = {'lvl': temp, 'wear': int(temp2)}
    scrapper.back()
    return car_stats

def scrap_weather(scrapper):
    weather_dict = dict()
    scrapper.find_element_by_link_text('Trening').click()
    with open('page.html', 'w') as file:
        file.write(scrapper.page_source)
    p = open('page.html', 'r')
    page = p.read()
    soup = BeautifulSoup(page, "html.parser")
    tds = soup.find_all("td")
    h2 = soup.find_all('h2')
    count = 0
    for i in h2:
        if count == 1:
            track = str(i.text.strip())
            gp = track.find(" GP")
            whitespace = track.rfind('\t')
            track = track[whitespace + 1:gp]
            weather_dict['track'] = track
            break
        count += 1
    count = 0
    for tr in tds:
        if count == 5 or count == 6:
            weather = str(tr).find('alt="')
            temp = str(tr).find('Temp: ')
            temp1 = str(tr).find('°')
            hum = str(tr).find('Wilgotność: ')
            hum1 = str(tr).find('%')
            weather = str(tr)[weather + 5]
            if weather == 'D':
                weather = 'wet'
            else:
                weather = 'dry'
            temp = int(str(tr)[temp + 6:temp1])
            hum = int(str(tr)[hum + 12:hum1])
            if count == 5:
                q = 'q1'
            else:
                q = 'q2'
            weather_dict[q] = {'weather': weather,
                                  'temp': temp,
                                  'hum': hum}
        count += 1
    scrapper.back()
    return weather_dict 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=800,800')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
scrapper = webdriver.Chrome(chrome_options=chrome_options)

