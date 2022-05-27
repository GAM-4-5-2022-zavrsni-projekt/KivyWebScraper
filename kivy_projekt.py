
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
import kivy
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
import json

import requests
from bs4 import BeautifulSoup


def moon():
    url = 'https://www.timeanddate.com/moon/phases/'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    faza = soup.find(id="cur-moon-percent").get_text()
    parent = soup.find(id='qlook').get_text()
    status = ''
    if 'Waxing' in parent or 'First' in parent:
        status = 'mjesec raste.'
    elif 'Waning' in parent or 'Third' in parent:
        status = 'mjesec pada.'

    return (f'Osvijetljenost Mjeseca: {faza} - {status}')


def sun():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    }

    url1 = "https://www.spaceweatherlive.com/includes/live-data.php?object=solar_flare&lang=EN"
    url2 = 'https://www.spaceweatherlive.com/includes/live-data.php?object=Plasma_Speed&lang=EN'
    #payload = {}
    headers = {
        'User-Agent': 'PostmanRuntime/7.29.0',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Host': 'www.spaceweatherlive.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    response = requests.get(url1, headers=headers)
    response2 = requests.get(url2, headers=headers)
    if str(response) == '<Response [200]>' and str(response2) == '<Response [200]>':
        data_dict = json.loads(response.text)
        data_dict2 = json.loads(response2.text)

        curr_val = data_dict['val']
        max2 = data_dict['val2']
        max24 = data_dict['val24']
        spd_val = data_dict2['val']

        soup = BeautifulSoup(curr_val, 'html.parser')
        curr_val = soup.find('div').text

        soup = BeautifulSoup(max2, 'html.parser')
        max2_val = soup.find('div').text

        soup = BeautifulSoup(max24, 'html.parser')
        max24_val = soup.find('div').text

        def check(value):
            if 'A' in value or 'B' in value:
                return 'Tiho'
            elif 'C' in value:
                return 'Mala baklja'
            elif 'M' in value:
                return 'Snažna baklja '
            elif 'X' in value:
                return 'Ogromna baklja'
        data = ''
        if int(spd_val) < 450:
            data = 'Normalna brzina'
        elif 700 > int(spd_val) > 450:
            data = 'Srednje velika brzina'
        elif 900 > int(spd_val) < 700:
            data = 'Velika brzina'
        elif int(spd_val) > 900:
            data = 'Jako velika brzina'
        status = f"          Trenutna vrijednost: {curr_val}            {check(curr_val)}\n          2h maks.: {max2_val}                             {check(max2_val)}\n          24h maks.: {max24_val}                             {check(max24_val)}\n          Sunčev vjetar: {spd_val} km/sec         {data}"
        # \n\n\nA & B = Quiet                     < 400 = Normalna brzina\nC = Mala baklja                 500 > = Srednje velika brzina\nM = Snažna baklja             700 > = Velika brzina\nX = Ogromna baklja           900 > = Jako velika brzina\n
        return status


kivy.require("1.9.1")


Config.set('graphics', 'resizable', True)
Window.clearcolor = (1, 1, 1, 1)


class RootWidget(RelativeLayout):

    def btn_clk(self):
        self.lbl.text = moon()

    def btn2_clk(self):
        self.lbl2.text = sun()


class ActionApp(App):

    def build(self):
        self.title = 'Web Scraper'
        self.icon = 'full-moon.png'
        return RootWidget()


# creating the myApp root for ActionApp() class
myApp = ActionApp()


myApp.run()
