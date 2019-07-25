# __init__.py

import os, sys

# Local imports
sys.path.insert(0,'..')

try:
    import controller, cli, lunchscraper
except:
    from lunchscraper import controller, cli, lunchscraper
