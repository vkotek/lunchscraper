# __main__.py
from datetime import datetime

try:
    import lunchscraper
except:
    from lunchscraper import lunchscraper

x = lunchscraper.lunchScraper()
x.scrape_restaurants()
result = x.send_messages_html()

print("[{}] Execution completed with {}.".format(datetime.now(), result) )
