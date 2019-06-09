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

    def add_menu(self, name, url, selector, n=0):
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
            self.data['body']['menus'].append({'name':name,'url':url,'menu':text})
        except Exception as e:
            print("Couldn't find menu for {}. Error: {}".format(name, e))

    def send_message(self):
        auth = ("api", SETTINGS.MAIL_API_KEY)
        data = {
            "from": SETTINGS.FROM,
            "to": self.get_recipients(SETTINGS.SUBSCRIBERS),
            "subject": self.data['title'],
            "h:X-Mailgun-Variables": json.dumps(self.data),
            "t:text": "yes",
            "template": "daily-menu",
        }
        r = requests.post(SETTINGS.MAIL_URL, auth=auth, data=data)
        return r

    def get_recipients(self, path_to_json):
        with open(path_to_json, 'r') as f:
            subscribers = json.load(f)
            recipients = []
            for subscriber in subscribers:
                recipients.append(subscriber['email'])
        return recipients

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
    weekday = weekday if int(weekday) <= 7 else 7
    temp.add_menu(name, url, selector, n=weekday)

    # Potrefena Husa - Na Verandach
    name = "Potrefena Husa - Na Verandach"
    url = "https://www.phnaverandach.cz/"
    selector = ".listek-out .listek #table-1 .food-title"
    temp.add_menu(name, url, selector, n=-1)

    # Lavande Restaurant - Weekly
    name = "Lavande Restaurant - Week"
    url = "https://restaurantlavande.cz/menu/#week-menu"
    selector = ".week-menu__header ~ .menus .menus__menu-content h3 ~ div .food__name"
    temp.add_menu(name, url, selector, n=range(0,3))

    # Lavande Restaurant - Daily
    name = "Lavande Restaurant - Week"
    url = "https://restaurantlavande.cz/menu/#week-menu"
    weekday = datetime.today().weekday()
    weekday = weekday if weekday < 5 else 4
    n = (( weekday + 1) * 4) - 1
    selector = ".week-menu__header ~ .menus .menus__menu-content h3 ~ div .food__name"
    temp.add_menu(name, url, selector, n=range(n,n+4))

if __name__ == "__main__":
    x = lunchScraper()
    your_restaurants(x)
    result = x.send_message()
    print("[{}] Execution completed with {}.".format(datetime.now(), result) )
