from lunchscraper import lunchScraper

temp = lunchScraper()

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
temp.add_menu(id, name, url, selector, n=-1)

# FIVE - Weekly
id = 3
name = "Dave B, Five (Week)"
language = "en"
url = "https://www.daveb.cz/cs/denni-nabidka"
selector = ".article .row div"
temp.add_menu(id, name, url, selector, n=1)

# FIVE - Today
id = 3
name = "Dave B, Five (Today)"
language = "en"
url = "https://www.daveb.cz/cs/denni-nabidka"
selector = ".article .row div"
weekday = 3 + datetime.today().weekday()
weekday = weekday if int(weekday) <= 7 else 7
temp.add_menu(id, name, url, selector, n=weekday)

# Potrefena Husa - Na Verandach
id = 4
name = "Potrefena Husa - Na Verandach"
language = "cs"
url = "https://www.phnaverandach.cz/"
selector = ".listek-out .listek #table-1 .food-title"
temp.add_menu(id, name, url, selector, n=-1)

# Lavande Restaurant - Weekly
id = 5
name = "Lavande Restaurant - Week"
language = "cs"
url = "https://restaurantlavande.cz/menu/#week-menu"
selector = ".week-menu__header ~ .menus .menus__menu-content h3 ~ div .food__name"
temp.add_menu(id, name, url, selector, n=range(0,3))

# Lavande Restaurant - Daily
id = 5
name = "Lavande Restaurant - Daily"
language = "cs"
url = "https://restaurantlavande.cz/menu/#week-menu"
weekday = datetime.today().weekday()
weekday = weekday if weekday < 5 else 4
n = (( weekday + 1) * 4) - 1
selector = ".week-menu__header ~ .menus .menus__menu-content h3 ~ div .food__name"
temp.add_menu(id, name, url, selector, n=range(n,n+4))

# Prostor
id = 6
name = "Prostor"
language = "cs"
url = "http://www.prostor.je"
selector = "#daily-menu ul"
temp.add_menu(id, name, url, selector, n=-1)

# Gourmet Pauza
id = 7
name = "Gourmet Pauza"
language = "cs"
url = "http://www.gourmetpauza.cz/"
selector = "#dish-tab-45 .stm_dish_name"
temp.add_menu(id, name, url, selector, n=-1)

# Erpet Golf Centrum
id = 8
name = "Erpet Golf Centrum"
language = "cs"
url = "http://erpetgolfcentrum.cz/cherry-services/poledni-menu/"
selector = "#cenik-listky"
temp.add_menu(id, name, url, selector, n=-1)

# Srdcovka Gurmania
id = 9
name = "Srdcovka Gurmania"
language = "cs"
url = "http://www.gambrinus.cz/srdcovka/gurmania/menu#obedovemenu"
selector = "#obedovemenu .menu-list-day > *"
temp.add_menu(id, name, url, selector, n=-1)
