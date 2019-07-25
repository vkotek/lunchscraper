# __main__.py

from datetime import datetime
import sys

# Local imports
sys.path.insert(0,'..')

try:
    import lunchscraper
except:
    from lunchscraper import lunchscraper

x = lunchscraper.lunchScraper()
x.scrape_restaurants()
result = x.send_messages_html()

print("[{}] Execution completed with {}.".format(datetime.now(), result) )
