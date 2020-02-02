from datetime import datetime

def scrape(temp, i):

    if not i or i == 1:
        # Pastva
        id = 1
        name = "Pastva"
        language = "cs"
        url = "https://www.facebook.com/Pastva%20/"
        location = "https://goo.gl/maps/UBEjpU1Dez3roc7a7"
        facebook = "https://www.facebook.com/Pastva%20/"
        temp.add_menu(id, language, name, url, selector=None, facebook=True, location=location)

    if not i or i == 2:
        # Sodexo
        id = 2
        name = "Sodexo, Riverview"
        language = "en"
        url = "http://riverview.extranet.prod.dator3.cz/en/menu-for-the-week/"
        weekday = 4 - datetime.today().weekday()
        weekday = weekday if weekday > 0 else 0
        selector = "#menu-{} .popisJidla".format(str(weekday))
        temp.add_menu(id, language, name, url, selector, n=-1, location=location)

    if not i or i == 3:
        # FIVE - Weekly
        id = 3
        name = "Dave B, Five (Week)"
        language = "cs"
        url = "https://www.daveb.cz/cs/denni-nabidka"
        location = "https://goo.gl/maps/7Rq6NGy15TqH5VYj8"
        selector = ".article .row div"
        temp.add_menu(id, language, name, url, selector, n=1, location=location)

        # FIVE - Today
        id = 3
        name = "Dave B, Five (Today)"
        language = "cs"
        url = "https://www.daveb.cz/cs/denni-nabidka"
        location = "https://goo.gl/maps/7Rq6NGy15TqH5VYj8"
        selector = "#first"
        weekday = -1
        temp.add_menu(id, language, name, url, selector, n=weekday, location=location)

    if not i or i == 4:
        # Potrefena Husa - Na Verandach
        id = 4
        name = "Potrefena Husa - Na Verandach"
        language = "cs"
        url = "https://www.phnaverandach.cz/"
        location = "https://goo.gl/maps/zgPNmN2ZgF9qxr2s8"
        selector = ".listek-out .listek #table-1 .food-title"
        temp.add_menu(id, language, name, url, selector, n=-1, location=location)

    if not i or i == 5:
        # Lavande Restaurant - Weekly
        id = 5
        name = "Lavande Restaurant - Week"
        language = "cs"
        url = "https://restaurantlavande.cz/menu/#week-menu"
        location = "https://goo.gl/maps/2eAVbJgxv3Sguhb48"
        selector = ".week-menu__header ~ .menus .menus__menu-content h3 ~ div .food__name"
        temp.add_menu(id, language, name, url, selector, n=range(0,3), location=location)

    if not i or i == 5:
        # Lavande Restaurant - Daily
        id = 5
        name = "Lavande Restaurant - Daily"
        language = "cs"
        url = "https://restaurantlavande.cz/menu/#week-menu"
        location = "https://goo.gl/maps/2eAVbJgxv3Sguhb48"
        weekday = datetime.today().weekday()
        weekday = weekday if weekday < 5 else 4
        n = (( weekday + 1) * 4) - 1
        selector = ".week-menu__header ~ .menus .menus__menu-content h3 ~ div .food__name"
        temp.add_menu(id, language, name, url, selector, n=range(n,n+4), location=location)

    if not i or i == 6:
        # Prostor
        id = 6
        name = "Prostor"
        language = "cs"
        url = "http://www.prostor.je"
        location = "https://goo.gl/maps/cXchX4Gi1FZzytrZA"
        selector = "#daily-menu ul"
        temp.add_menu(id, language, name, url, selector, n=-1, location=location)

    if not i or i == 7:
        # Gourmet Pauza
        id = 7
        name = "Gourmet Pauza"
        language = "cs"
        url = "http://www.gourmetpauza.cz/"
        location = "https://goo.gl/maps/XDQD61g9LVb7ARi67"
        selector = "#dish-tab-45 .stm_dish_name"
        temp.add_menu(id, language, name, url, selector, n=-1, location=location)

    if not i or i == 8:
        # Erpet Golf Centrum
        id = 8
        name = "Erpet Golf Centrum"
        language = "cs"
        url = "http://erpetgolfcentrum.cz/cherry-services/poledni-menu/"
        location = "https://goo.gl/maps/T3nUDsWd1PgMDozs5"
        selector = "#cenik-listky"
        temp.add_menu(id, language, name, url, selector, n=-1)

    if not i or i == 9:
        # Srdcovka Gurmania
        id = 9
        name = "Srdcovka Gurmania"
        language = "cs"
        url = "http://www.gambrinus.cz/srdcovka/gurmania/menu#obedovemenu"
        location = "https://goo.gl/maps/iLNzNvCyD8yrqwHj9"
        selector = "#obedovemenu .menu-list-day > *"
        temp.add_menu(id, language, name, url, selector, n=-1, location=location)

    if not i or i == 10:
        # Tradice
        id = 10
        name = "Tradice"
        language = "cs"
        url = "http://tradiceandel.cz/cz/denni-nabidka/"
        location = "https://goo.gl/maps/1HQBJshEqWWaHJT9A"
        selector = ".content.menu"
        temp.add_menu(id, language, name, url, selector, n=-1, location=location)

    if not i or i == 11:
        # Eaternia
        id = 11
        name = "Eaternia"
        language = "cs"
        url = "https://www.eterniasmichov.com/eaternia-jidelna"
        location = "https://g.page/EATERNIA?share"
        selector = '.dropdown ~ div[class$="PoledniMenu"] > div'
        temp.add_menu(id, language, name, url, selector, n=-1, javascript=True, location=location)

    if not i or i == 12:
        # Smichovna
        id = 12
        name = "Smíchovna"
        language = "cs"
        url = "https://www.smichovna.cz"
        location = "https://goo.gl/maps/Guc9Ud835FCNDJ34A"
        selector = '#menudaily table span'
        temp.add_menu(id, language, name, url, selector, n=-1, javascript=False, location=location)

    if not i or i == 13:
        # The Pub
        id = 13
        name = "The Pub"
        language = "cs"
        url = "https://www.thepub.cz/praha-5/?lng=cs"
        location = "https://goo.gl/maps/GTKuFA52RVPSiYSc9"
        selector = '.menu-today-data ol'
        temp.add_menu(id, language, name, url, selector, n=-1, javascript=False, location=location)

    if not i or i == 14:
        # Corleone
        id = 14
        name = "Corleone"
        language = "cs"
        url = "https://www.corleone.cz/pizzeria-andel/obedova-nabidka"
        location = "https://goo.gl/maps/iKZHEXFfGcXNbsNL6"
        selector = ".restaurant-menuweek th, .restaurant-menuweek td"
        temp.add_menu(id, language, name, url, selector, n=-1, javascript=False, location=location)

    if not i or i == 15:
        # Plzenska Restaurace Andel
        id = 15
        name = "Plzeňský restaurant Anděl"
        language = "cs"
        url = "https://www.restauraceandel.cz/"
        location = "https://goo.gl/maps/Wt4SnL1tnAFaAjJb9"  
        weekday = datetime.today().weekday() + 1
        weekday = weekday if weekday < 5 else 5
        selector = "#denni .tab-content div:nth-of-type({weekday}) table:nth-of-type(n+2) tr td:nth-of-type(2)".format(weekday=weekday)
        temp.add_menu(id, language, name, url, selector, n=-1, javascript=False, location=location)


    # if not i or i == 15:
    #     # U Kroka
    #     id = 15
    #     name = "U Kroka"
    #     language = "cs"
    #     url = "https://www.ukroka.cz/menus-1"
    #     selector = 'iframe[title="Menus"]'
    #     foo = temp.scrape_menu("self", url, selector, javascript=True)
    #     selector = 'li[data-hook="wixrest-menus-item"]'
    #     temp.add_menu(id, language, name, url, selector, n=-1, javascript=True)
