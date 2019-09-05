# lunchscraper.py

from urllib import request
from bs4 import BeautifulSoup as bs
from datetime import datetime
from jinja2 import Template
import requests
import json
import logging
import os, sys
from unidecode import unidecode

# Local imports
sys.path.insert(0,'..')

import settings as SETTINGS
import controller, translator
# try:
#     import controller, translator
# except:
#     from lunchscraper import controller, translator

SUBSCRIBERS = os.path.abspath(SETTINGS.SUBSCRIBERS)

class lunchScraper(object):

    def __init__(self):
        self.data = {
            "title": "Daily Menu for {}".format(datetime.now().strftime("%A, %d-%b")),
            "body": {
                "menus": []
            }
        }
        self.menus = [] # New data structure
        self.settings = SETTINGS

    def add_menu(self, id, language, name, url, selector, n=0):
        """
        id       :: id of the restaurant, used for grouping and hiding restaurants.
        name     :: name of the restaurant
        url      :: the URL where the menu can be found
        selector :: CSS selector to find menu on page
        n        :: specifies how to handle results

        n = 0 [DEFAULT]
        Gets the first element in the response.

        n = -1
        Combines the text in all found elements.

        n = range(x, y)
        Fetches tech from elements x through y from the response."""

        try:
            text_raw = self.scrape_menu( url, selector)

            text_list = self.convert_to_list( text_raw, n)

            # Checks if menu is for more days, extracts today's menu.
            text_menu = self.get_today_items( text_list)

            # Remove any short list items (i.e. prices)
            text_menu = [ t for t in text_menu if len(t) > 10]

            # Translate to Czech / English
            target_language = 'cs' if language == 'en' else 'en'

            if language == 'cs':
                text_menu_cs = text_menu
                text_menu_en = translator.translate(text_menu, 'cs', 'en')
            elif language == 'en':
                text_menu_en = text_menu
                text_menu_cs = translator.translate(text_menu, 'en', 'cs')

            if not isinstance(text_menu, list):
                raise Exception('Scraped Menu: Expected list, got {}.'.format(type(text_menu)))

            self.menus.append(
                {
                    'id':id,
                    'name':name,
                    'url':url,
                    'menu':text_menu,
                    'menu_cs': text_menu_cs,
                    'menu_en': text_menu_en,
                })

        except Exception as e:
            print("Couldn't find menu for {}. Error: {}".format(name, e))


    def scrape_menu(self, url, selector):
        try:
            with request.urlopen(url) as response:
                html = response.read()
                soup = bs(html, 'lxml')
                selected = soup.select(selector)

            return selected

        except:
            raise Exception("Unable to retrieve menu from URL. ({})".format(url))

    def convert_to_list(self, raw_text, n=0):

        if not isinstance(raw_text, list):
            raw_text2 = [raw_text]

        if n == -1:
            text = "\n".join([item.get_text() for item in raw_text])

        elif isinstance(n, range):
            text = []
            for i in n:
                text.append( clean(raw_text[i].get_text()) )
            text = "\n".join(text)

        else:
            text = raw_text[n]
            text = str(text).replace("<br/>", "\n")
            text = bs(text, 'lxml').get_text()

        text = [ self.trim(t) for t in text.split("\n") if len(t) > 0]

        return text

    @staticmethod
    def trim(txt):

        if not isinstance(txt, str):
            return txt

        def trim_left(txt):
            if not txt[0].isalnum():
                return lunchScraper.trim(txt[1:])
            else:
                return txt

        def trim_right(txt):
            if not txt[-1].isalnum():
                return lunchScraper.trim(txt[:-1])
            else:
                return txt

        return trim_left(trim_right(txt))


    def send_messages(self):

        recipients = self.get_recipients()

        auth = ("api", self.settings.MAIL_API_KEY)
        results = {}

        for recipient in recipients:
            menus = [r for r in self.data['body']['menus'] if str(r['id']) in recipient['preferences']]
            data = { 'body': {
                'menus': menus,
                'token': recipient['token'],
            }, 'title': self.data['title'],
            }
            config = {
                "from": self.settings.FROM,
                "to": recipient['email'],
                "subject": self.data['title'],
                "h:X-Mailgun-Variables": json.dumps(data),
                "t:text": "yes",
                "template": "daily-menu",
            }
            r = requests.post(self.settings.MAIL_URL, auth=auth, data=config)

        return True

    def send_messages_html(self, email=None):

        if email:
            users = controller.User()
            user = users.get(email=email)
            if not user:
                user = users.add(email, verify=True)
            recipients = [user]
        else:
            recipients = self.get_recipients()

        auth = ("api", self.settings.MAIL_API_KEY)

        notice = controller.Email.get_notice()

        send_counter = 0

        for recipient in recipients:

            print( "Sending email to {}.".format(recipient['email']) )

            # Get menus for preferences of given user
            menus = [r for r in self.menus if str(r['id']) in recipient['preferences']]

            if recipient['language'] in ['cs', 'en']: # Check if language is set for user.
                language = str('menu_' + recipient['language'])
            else: # Use original menu language
                language = 'menu'
            for menu in menus:
                menu['menu'] = menu[language]

            data = {
                'title': "Daily Menu for {}".format(datetime.now().strftime("%A, %d-%b")),
                'notice': notice,
                'recipient': {
                    'email': recipient['email'],
                    'url': SETTINGS.URL + "/edit?token=" + recipient['token'],
                },
                'menus': menus,
                'language': language,
            }

            # Generate html email template for user with given data
            email_html = self.render_email('master.html', data)

            config = {
                "from": self.settings.FROM,
                "to": recipient['email'],
                "subject": self.data['title'],
                "html": email_html,
            }
            r = requests.post(self.settings.MAIL_URL, auth=auth, data=config)

            if r.status_code == 200:
                send_counter += 1

        print("{} / {} Emails sent successfully.".format( send_counter, len(recipients) ) )

        return True

    def get_recipients(self):

        file = SETTINGS.SUBSCRIBERS

        with open(file, 'r') as f:
            subscribers = json.load(f)
        return subscribers

    def render_email(self, template, data):

        with open("templates/"+template, 'r') as html:
            html = html.read()
            template = Template(html)
            html = template.render(data=data)

        return html

    def scrape_restaurants(self):
        your_restaurants(self)

    def wday_to_text(self, weekday):
        """
        Converts int of weekday into list of text versions of given day.
        """
        if weekday == 0:
            return ["pondeli","pondělí", "monday"]
        elif weekday == 1:
            return ["utery","úterý", "tuesday"]
        elif weekday == 2:
            return ["streda","středa", "wednesday", "středu"]
        elif weekday == 3:
            return ["ctvrtek","čtvrtek", "thursday"]
        elif weekday == 4:
            return ["patek","pátek", "friday"]
        elif weekday == 5:
            return ["sobota","sobota", "saturday", "sobotu"]
        elif weekday == 6:
            return ["nedele","neděle", "sunday", "neděli"]
        else:
            return [""]

    def day_found(self, text, day):
        for lang in day:
            if unidecode( text.lower( ) ).find( lang ) >= 0:
                return True

    def get_today_items(self, menu_list):
        """
        Check if menu is for multiple days, extract and return today's menu items.
        """

        weekday = datetime.today().weekday()

        today, tomorrow = self.wday_to_text(weekday), self.wday_to_text(weekday+1)

        menu_text = ";".join(menu_list).lower()

        # Check if at today is mentioned on the menu. If yes, continue.
        if not self.day_found(menu_text, today):
            return menu_list

        start, end = None, None
        for i, item in enumerate(menu_list):
            if self.day_found(item, today):
                start = i + 1
            elif self.day_found(item, tomorrow):
                end = i

        return menu_list[start:end]

def clean(string):
    return "".join([char for char in string if char.isalnum() or char == " "])

def your_restaurants(temp):

    # Pastva
    id = 1
    name = "Pastva"
    language = "cs"
    url = "https://www.pastva-restaurant.cz/nase-menu/"
    selector = "#cff .cff-text"
    temp.add_menu(id, language, name, url, selector)

    # Sodexo
    id = 2
    name = "Sodexo, Riverview"
    language = "en"
    url = "http://riverview.extranet.prod.dator3.cz/en/menu-for-the-week/"
    weekday = 4 - datetime.today().weekday()
    weekday = weekday if weekday > 0 else 0
    tag = "#menu-{} .popisJidla".format(str(weekday))
    selector = tag
    temp.add_menu(id, language, name, url, selector, n=-1)

    # FIVE - Weekly
    id = 3
    name = "Dave B, Five (Week)"
    language = "en"
    url = "https://www.daveb.cz/cs/denni-nabidka"
    selector = ".article .row div"
    temp.add_menu(id, language, name, url, selector, n=1)

    # FIVE - Today
    id = 3
    name = "Dave B, Five (Today)"
    language = "en"
    url = "https://www.daveb.cz/cs/denni-nabidka"
    selector = ".article .row div"
    weekday = 3 + datetime.today().weekday()
    weekday = weekday if int(weekday) <= 7 else 7

    selector = "#first"
    weekday = -1
    temp.add_menu(id, language, name, url, selector, n=weekday)

    # Potrefena Husa - Na Verandach
    id = 4
    name = "Potrefena Husa - Na Verandach"
    language = "cs"
    url = "https://www.phnaverandach.cz/"
    selector = ".listek-out .listek #table-1 .food-title"
    temp.add_menu(id, language, name, url, selector, n=-1)

    # Lavande Restaurant - Weekly
    id = 5
    name = "Lavande Restaurant - Week"
    language = "cs"
    url = "https://restaurantlavande.cz/menu/#week-menu"
    selector = ".week-menu__header ~ .menus .menus__menu-content h3 ~ div .food__name"
    temp.add_menu(id, language, name, url, selector, n=range(0,3))

    # Lavande Restaurant - Daily
    id = 5
    name = "Lavande Restaurant - Daily"
    language = "cs"
    url = "https://restaurantlavande.cz/menu/#week-menu"
    weekday = datetime.today().weekday()
    weekday = weekday if weekday < 5 else 4
    n = (( weekday + 1) * 4) - 1
    selector = ".week-menu__header ~ .menus .menus__menu-content h3 ~ div .food__name"
    temp.add_menu(id, language, name, url, selector, n=range(n,n+4))

    # Prostor
    id = 6
    name = "Prostor"
    language = "cs"
    url = "http://www.prostor.je"
    selector = "#daily-menu ul"
    temp.add_menu(id, language, name, url, selector, n=-1)

    # Gourmet Pauza
    id = 7
    name = "Gourmet Pauza"
    language = "cs"
    url = "http://www.gourmetpauza.cz/"
    selector = "#dish-tab-45 .stm_dish_name"
    temp.add_menu(id, language, name, url, selector, n=-1)

    # Erpet Golf Centrum
    id = 8
    name = "Erpet Golf Centrum"
    language = "cs"
    url = "http://erpetgolfcentrum.cz/cherry-services/poledni-menu/"
    selector = "#cenik-listky"
    temp.add_menu(id, language, name, url, selector, n=-1)

    # Srdcovka Gurmania
    id = 9
    name = "Srdcovka Gurmania"
    language = "cs"
    url = "http://www.gambrinus.cz/srdcovka/gurmania/menu#obedovemenu"
    selector = "#obedovemenu .menu-list-day > *"
    temp.add_menu(id, language, name, url, selector, n=-1)

if __name__ == "__main__":
    x = lunchScraper()
    x.scrape_restaurants()
    result = x.send_messages_html()
    print("[{}] Execution completed with {}.".format(datetime.now(), result) )
