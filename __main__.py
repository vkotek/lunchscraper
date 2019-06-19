# Lunch Menu Scraper

from urllib import request
from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests
import json
import logging

import settings as SETTINGS

class lunchScraper(object):

    def __init__(self):
        self.data = {
            "title": "Daily Menu for {}".format(datetime.now().strftime("%A, %d-%b")),
            "body": {
                "menus": []
            }
        }

    def add_menu(self, id, name, url, selector, n=0):
        try:
            with request.urlopen(url) as response:
                html = response.read()
                soup = bs(html, 'lxml')
                selected = soup.select(selector)
                if n == -1:
                    text = "\n".join([item.get_text() for item in selected])
                elif isinstance(n, range):
                    text = []
                    for i in n:
                        text.append( clean(selected[i].get_text()) )
                    text = "\n".join(text)
                else:
                    text = selected[n].get_text()
                text = [t for t in text.split("\n") if len(t) > 0]
            self.data['body']['menus'].append({'id':id,'name':name,'url':url,'menu':text})
        except Exception as e:
            print("Couldn't find menu for {}. Error: {}".format(name, e))

    def send_messages(self):

        recipients = self.get_recipients()

        auth = ("api", SETTINGS.MAIL_API_KEY)
        results = {}

        for recipient in recipients:
            menus = [r for r in self.data['body']['menus'] if str(r['id']) in recipient['preferences']]
            data = { 'body': {
                'menus': menus,
                'token': recipient['token'],
            }, 'title': self.data['title'],
            }
            config = {
                "from": SETTINGS.FROM,
                "to": recipient['email'],
                "subject": self.data['title'],
                "h:X-Mailgun-Variables": json.dumps(data),
                "t:text": "yes",
                "template": "daily-menu",
            }
            r = requests.post(SETTINGS.MAIL_URL, auth=auth, data=config)

        return True

    def get_recipients(self):
        with open(SETTINGS.SUBSCRIBERS, 'r') as f:
            subscribers = json.load(f)
        return subscribers

def clean(string):
    return "".join([char for char in string if char.isalnum() or char == " "])

def your_restaurants(temp):

    # Pastva
    id = 1
    name = "Pastva"
    url = "https://www.pastva-restaurant.cz/nase-menu/"
    selector = "#ffe_widget-2 .eff-panel-body"
    temp.add_menu(id, name, url, selector)

    # Sodexo
    id = 2
    name = "Sodexo, Riverview"
    url = "http://riverview.extranet.prod.dator3.cz/en/menu-for-the-week/"
    weekday = 4 - datetime.today().weekday()
    weekday = weekday if weekday > 0 else 0
    tag = "#menu-{} .popisJidla".format(str(weekday))
    selector = tag
    temp.add_menu(id, name, url, selector, n=-1)

    # FIVE - Weekly
    id = 3
    name = "Dave B, Five (Week)"
    url = "https://www.daveb.cz/cs/denni-nabidka"
    selector = ".article .row div"
    temp.add_menu(id, name, url, selector, n=1)

    # FIVE - Today
    id = 3
    name = "Dave B, Five (Today)"
    url = "https://www.daveb.cz/cs/denni-nabidka"
    selector = ".article .row div"
    weekday = 3 + datetime.today().weekday()
    weekday = weekday if int(weekday) <= 7 else 7
    temp.add_menu(id, name, url, selector, n=weekday)

    # Potrefena Husa - Na Verandach
    id = 4
    name = "Potrefena Husa - Na Verandach"
    url = "https://www.phnaverandach.cz/"
    selector = ".listek-out .listek #table-1 .food-title"
    temp.add_menu(id, name, url, selector, n=-1)

    # Lavande Restaurant - Weekly
    id = 5
    name = "Lavande Restaurant - Week"
    url = "https://restaurantlavande.cz/menu/#week-menu"
    selector = ".week-menu__header ~ .menus .menus__menu-content h3 ~ div .food__name"
    temp.add_menu(id, name, url, selector, n=range(0,3))

    # Lavande Restaurant - Daily
    id = 5
    name = "Lavande Restaurant - Daily"
    url = "https://restaurantlavande.cz/menu/#week-menu"
    weekday = datetime.today().weekday()
    weekday = weekday if weekday < 5 else 4
    n = (( weekday + 1) * 4) - 1
    selector = ".week-menu__header ~ .menus .menus__menu-content h3 ~ div .food__name"
    temp.add_menu(id, name, url, selector, n=range(n,n+4))
    
    # Prostor
    id = 6
    name = "Prostor"
    url = "http://www.prostor.je"
    selector = "#daily-menu ul"
    temp.add_menu(id, name, url, selector, n=-1)
    
if __name__ == "__main__":
    x = lunchScraper()
    your_restaurants(x)
    result = x.send_messages()
    print("[{}] Execution completed with {}.".format(datetime.now(), result) )
