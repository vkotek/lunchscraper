# lunchscraper.py

from urllib import request
import requests
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

# import settings as SETTINGS
# import controller, translator

try:
    import settings as SETTINGS
    import controller, translator, restaurants
except:
    from lunchscraper import settings as SETTINGS
    from lunchscraper import controller, translator, restaurants

# SUBSCRIBERS = os.path.abspath(SETTINGS.SUBSCRIBERS)

class lunchScraper(object):

    def __init__(self):
        self.menus = []
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

        print("[{}] Fetching menu for {}".format(id, name.ljust(30)), end="")
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
                # text_menu_es = translator.translate(text_menu, 'cs', 'es')
            elif language == 'en':
                text_menu_en = text_menu
                text_menu_cs = translator.translate(text_menu, 'en', 'cs')
                # text_menu_es = translator.translate(text_menu, 'en', 'es')

            if not isinstance(text_menu, list):
                print('ERROR: NOT A LIST ({})'.format(type(text_menu)))
                return False
                # raise Exception('Scraped Menu: Expected list, got {}.'.format(type(text_menu)))

            self.menus.append(
                {
                    'id':id,
                    'name':name,
                    'url':url,
                    'menu':text_menu,
                    'menu_cs': text_menu_cs,
                    'menu_en': text_menu_en,
                    # 'menu_es': text_menu_es,
                })

            print("OK!")
            return True

        except Exception as e:
            print("Couldn't get menu for {}. Error: {}".format(name, e))


    def scrape_menu(self, url, selector):
        try:
            # with request.urlopen(url) as response:
            with requests.get(url, timeout=9) as response:
                response.encoding = 'UTF-8'
                html = response.text
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
                text.append( self.clean(raw_text[i].get_text()) )
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

        recipients = [recipient for recipient in recipients if recipient['verified'] is not False]

        for recipient in recipients:

            try:

                print( "Sending email to {}".format(recipient['email'].ljust(40, ".") ), end="")

                # Get menus for preferences of given user
                menus = [r for r in self.menus if str(r['id']) in recipient['preferences']]

                # Define language so it corresponds to dictionary keys of languages in menu dict
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
                    "subject": "Daily Menu for {}".format(datetime.now().strftime("%A, %d-%b")),
                    "html": email_html,
                }
                r = requests.post(self.settings.MAIL_URL, auth=auth, data=config)

                if r.status_code == 200:
                    send_counter += 1
                    print("OK!")
                else:
                    print("FAILED ({})".format(str(r.status_code)))

            except Exception as e:
                print("ERROR: {}".format(str(e)))


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

    def scrape_restaurants(self, id=None):
        restaurants.scrape(self, id)

    @staticmethod
    def wday_to_text(weekday):
        """
        Converts int of weekday into list of text versions of given day.
        """
        if weekday == 0:
            return ["pondeli",  "pondělí",  "pondělní",                 "monday"]
        elif weekday == 1:
            return ["utery",    "úterý",    "úterní",                   "tuesday"]
        elif weekday == 2:
            return ["streda",   "středa",   "středeční",    "středu",   "wednesday"]
        elif weekday == 3:
            return ["ctvrtek",  "čtvrtek",  "čtvrteční",                "thursday"]
        elif weekday == 4:
            return ["patek",    "pátek",    "páteční",                  "friday"]
        elif weekday == 5:
            return ["sobota",   "sobota",   "sobotní",      "sobotu",   "saturday"]
        elif weekday == 6:
            return ["nedele",   "neděle",   "nedělní",      "neděli",   "sunday"]
        else:
            return [""]

    @staticmethod
    def day_found(text, day):
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

    def save_menu(self):

        filename = "data/menu.json"
        print("Attempting to save menu to {}..".format( os.path.abspath(filename)) )

        data = {
            'date': datetime.now().strftime("%A (%Y-%m-%d)"),
            'menus': self.menus
        }

        try:
            with open(filename, "w+") as f:
                json.dump(data, f)
            print ("OK!")
            return True
        except Exception as e:
            print ("Error occured during saving:", e)
            return False

    @staticmethod
    def clean(string):
        return "".join([char for char in string if char.isalnum() or char == " "])

if __name__ == "__main__":
    print("[{}] Execution started".format(datetime.now()) )
    x = lunchScraper()
    x.scrape_restaurants()
    x.save_menu()
    x.send_messages_html()
    print("[{}] Execution completed".format(datetime.now()) )
