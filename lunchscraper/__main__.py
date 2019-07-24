# __main__.py

import lunchscraper
from datetime import datetime

x = lunchscraper.lunchScraper()
x.scrape_restaurants()
result = x.send_messages_html()

print("[{}] Execution completed with {}.".format(datetime.now(), result) )
