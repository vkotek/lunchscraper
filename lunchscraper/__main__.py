# __main__.py

from datetime import datetime
import sys

# Local imports
sys.path.insert(0,'..')

try:
    import lunchscraper
except:
    from lunchscraper import lunchscraper


print("[{}] Execution started".format(datetime.now()) )
x = lunchscraper.lunchScraper()
x.scrape_restaurants()
x.save_menu()
# x.send_messages_html()
print("[{}] Execution completed".format(datetime.now()) )
