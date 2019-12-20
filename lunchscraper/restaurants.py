### This is probably the best way to tackle this, and then have another file import this and iterate over the functions in it? To be tested.

from datetime import datetime

def scrape(temp, i):

    if not i or i == 1:
        # Pastva
        id = 1
        name = "Pastva"
        language = "cs"
        url = "https://www.pastva-restaurant.cz/nase-menu/"
        selector = "#cff .cff-text"
        temp.add_menu(id, language, name, url, selector)

    if not i or i == 2:
        # Sodexo
        id = 2
        name = "Sodexo, Riverview"
        language = "en"
        url = "http://riverview.extranet.prod.dator3.cz/en/menu-for-the-week/"
        weekday = 4 - datetime.today().weekday()
        weekday = weekday if weekday > 0 else 0
        selector = "#menu-{} .popisJidla".format(str(weekday))
        temp.add_menu(id, language, name, url, selector, n=-1)

    if not i or i == 3:
        # FIVE - Weekly
        id = 3
        name = "Dave B, Five (Week)"
        language = "cs"
        url = "https://www.daveb.cz/cs/denni-nabidka"
        selector = ".article .row div"
        temp.add_menu(id, language, name, url, selector, n=1)

        # FIVE - Today
        id = 3
        name = "Dave B, Five (Today)"
        language = "cs"
        url = "https://www.daveb.cz/cs/denni-nabidka"
        selector = "#first"
        weekday = -1
        temp.add_menu(id, language, name, url, selector, n=weekday)

    if not i or i == 4:
        # Potrefena Husa - Na Verandach
        id = 4
        name = "Potrefena Husa - Na Verandach"
        language = "cs"
        url = "https://www.phnaverandach.cz/"
        selector = ".listek-out .listek #table-1 .food-title"
        temp.add_menu(id, language, name, url, selector, n=-1)

    if not i or i == 5:
        # Lavande Restaurant - Weekly
        id = 5
        name = "Lavande Restaurant - Week"
        language = "cs"
        url = "https://restaurantlavande.cz/menu/#week-menu"
        selector = ".week-menu__header ~ .menus .menus__menu-content h3 ~ div .food__name"
        temp.add_menu(id, language, name, url, selector, n=range(0,3))

    if not i or i == 5:
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

    if not i or i == 6:
        # Prostor
        id = 6
        name = "Prostor"
        language = "cs"
        url = "http://www.prostor.je"
        selector = "#daily-menu ul"
        temp.add_menu(id, language, name, url, selector, n=-1)

    if not i or i == 7:
        # Gourmet Pauza
        id = 7
        name = "Gourmet Pauza"
        language = "cs"
        url = "http://www.gourmetpauza.cz/"
        selector = "#dish-tab-45 .stm_dish_name"
        temp.add_menu(id, language, name, url, selector, n=-1)

    if not i or i == 8:
        # Erpet Golf Centrum
        id = 8
        name = "Erpet Golf Centrum"
        language = "cs"
        url = "http://erpetgolfcentrum.cz/cherry-services/poledni-menu/"
        selector = "#cenik-listky"
        temp.add_menu(id, language, name, url, selector, n=-1)

    if not i or i == 9:
        # Srdcovka Gurmania
        id = 9
        name = "Srdcovka Gurmania"
        language = "cs"
        url = "http://www.gambrinus.cz/srdcovka/gurmania/menu#obedovemenu"
        selector = "#obedovemenu .menu-list-day > *"
        temp.add_menu(id, language, name, url, selector, n=-1)

    if not i or i == 10:
        # Tradice
        id = 10
        name = "Tradice"
        language = "cs"
        url = "http://tradiceandel.cz/cz/denni-nabidka/"
        selector = ".content.menu"
        temp.add_menu(id, language, name, url, selector, n=-1)

    if not i or i == 11:
        # Eaternia
        id = 11
        name = "Eaternia"
        language = "cs"
        url = "https://www.eterniasmichov.com/eaternia-jidelna"
        selector = '.dropdown ~ div[class$="PoledniMenu"] > div'
        temp.add_menu(id, language, name, url, selector, n=-1, javascript=True)

    if not i or i == 12:
        # Smichovna
        id = 12
        name = "Smíchovna"
        language = "cs"
        url = "https://www.smichovna.cz"
        selector = '#menudaily table span'
        temp.add_menu(id, language, name, url, selector, n=-1, javascript=False)


    if not i or i == 13:
        # Smichovna
        id = 13
        name = "The Pub"
        language = "cs"
        url = "https://www.thepub.cz/praha-5/?lng=cs"
        selector = '.menu-today-data ol'
        temp.add_menu(id, language, name, url, selector, n=-1, javascript=False)

    # if not i or i == 12 and False:
    #     # U Kroka
    #     id = 12
    #     name = "U Kroka"
    #     language = "cs"
    #     url = "https://www.ukroka.cz/menus-1"
    #     selector = 'iframe[title="Menus"]'
    #     foo = temp.scrape_menu("self", url, selector, javascript=True)
    #     selector = 'li[data-hook="wixrest-menus-item"]'
    #     temp.add_menu(id, language, name, url, selector, n=-1, javascript=True)
