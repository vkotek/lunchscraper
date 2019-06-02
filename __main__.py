# Lunch Menu Scraper

from urllib import request
from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests
import json

import settings as SETTINGS

class lunchScraper(object):
    
    def __init__(self):
        self.data = {
            "title": "Daily Menu for {}".format(datetime.now().strftime("%A, %d-%b")),
            "body": {
                "menus": []
            }
        }
        
    def add_menu(self, name, url, selector, n=0):
        try:
            with request.urlopen(url) as response:
                html = response.read()
                soup = bs(html, 'lxml')
                selected = soup.select(selector)
                if n == -1:
                    text = "\n".join([item.get_text() for item in selected])
                else:
                    text = selected[n].get_text()
                text = [t for t in text.split("\n") if len(t) > 0]
            self.data['body']['menus'].append({'name':name,'url':url,'menu':text})
        except Exception as e:
            print("Couldn't find menu for {}. Error: {}".format(name, e))

    def send_message(self):
        auth = ("api", SETTINGS.MAIL_API_KEY)
        data = {
            "from": SETTINGS.FROM,
            "to": SETTINGS.TO,
            "subject": self.data['title'],
            "h:X-Mailgun-Variables": json.dumps(self.data),
            "t:text": "yes",
            "template": "daily-menu",
        }
        r = requests.post(SETTINGS.MAIL_URL, auth=auth, data=data)
        return r
    
def your_restaurants(temp):

    # Pastva
    name = "Pastva"
    url = "https://www.pastva-restaurant.cz/nase-menu/"
    selector = "#ffe_widget-2 .eff-panel-body"
    temp.add_menu(name, url, selector)

    # Sodexo
    name = "Sodexo, Riverview"
    url = "http://riverview.extranet.prod.dator3.cz/en/menu-for-the-week/"
    weekday = 4 - datetime.today().weekday()
    weekday = weekday if weekday > 0 else 0
    tag = "#menu-{} .popisJidla".format(str(weekday))
    selector = tag
    temp.add_menu(name, url, selector, n=-1)

    # FIVE - Weekly
    name = "Dave B, Five (Week)"
    url = "https://www.daveb.cz/cs/denni-nabidka"
    selector = ".article .row div"
    temp.add_menu(name, url, selector, n=1)

    # FIVE - Today
    name = "Dave B, Five (Today)"
    url = "https://www.daveb.cz/cs/denni-nabidka"
    selector = ".article .row div"
    weekday = 3 + datetime.today().weekday()
    weekday = weekday if int(weekday) <= 7 else 3
    temp.add_menu(name, url, selector, n=weekday)

if __name__ == "__main__":
    x = lunchScraper()
    your_restaurants(x)
    x.send_message()